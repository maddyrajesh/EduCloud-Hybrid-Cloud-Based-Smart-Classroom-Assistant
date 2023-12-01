import os
import logging
import pickle
import tempfile
import boto3
import face_recognition

# Constants for S3 bucket names and timeout
INPUT_BUCKET_NAME = "546proj2inputbucket-1"
OUTPUT_BUCKET_NAME = "546proj2outputbucket-1"
SIGNED_URL_TIMEOUT = 5000

# Initialize boto3 clients
s3 = boto3.client('s3', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def open_encoding(filename):
    """
    Opens a file containing encoded face data.

    Args:
        filename (str): The path to the file to be opened.

    Returns:
        data: The data loaded from the file.
    """
    try:
        with open(filename, "rb") as file:
            data = pickle.load(file)
        return data
    except Exception as e:
        logging.error(f"Error loading encoding file: {e}")
        raise

def get_first_file(bucket_name):
    """
    Gets the first file from the specified S3 bucket.

    Args:
        bucket_name (str): Name of the S3 bucket.

    Returns:
        str: The key of the first file, or None if no files are found.
    """
    response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
    files = [obj['Key'] for obj in response.get('Contents', [])]
    return files[0] if files else None

def face_recognition_handler(bucket, key):
    try:
        logging.info("Processing face_recognition_handler")

        video_basename = os.path.splitext(key)[0]  # Extract base name of the video file

        with tempfile.TemporaryDirectory() as dir:
            video_path = os.path.join(dir, key)
            s3.download_file(bucket, key, video_path)

            # Extract only the first frame from video
            ffmpeg_cmd = f"ffmpeg -i {video_path} -vframes 1 {dir}/{video_basename}_frame.jpeg"
            os.system(ffmpeg_cmd)

            # Process the extracted frame
            frame_file = f"{video_basename}_frame.jpeg"
            process_image(dir, frame_file)


    except Exception as e:
        logging.error("Exception occurred in face_recognition_handler", exc_info=True)
        return {'statusCode': 500, 'body': f'Error processing the video: {e}'}

    return {'statusCode': 200, 'body': f'CSV file {video_basename}.csv generated and uploaded to S3'}




def process_image(dir, image):
    """
    Processes an individual image for face recognition.

    Args:
        dir (str): The directory where the image is located.
        image (str): The image file name.
    """
    try:
        unknown_image = face_recognition.load_image_file(os.path.join(dir, image))
        face_locations = face_recognition.face_locations(unknown_image)
        unknown_image_encoding = face_recognition.face_encodings(unknown_image, face_locations)

        script_dir = os.path.dirname(__file__)
        encoding_lists = open_encoding(os.path.join(script_dir, "encoding"))

        for face_encoding in unknown_image_encoding:
            results = face_recognition.compare_faces(encoding_lists['encoding'], face_encoding)
            matching_names = [name for i, name in enumerate(encoding_lists['name']) if results[i]][0]
            logging.info(f'Found matching names: {matching_names}')

            response = dynamodb.scan(
                TableName='student_data',
                FilterExpression='#n = :name',
                ExpressionAttributeNames={'#n': 'name'},
                ExpressionAttributeValues={':name': {'S': matching_names}}
            )

            student_info = format_student_info(response)
            upload_csv(student_info, image)
    except Exception as e:
        logging.error(f"Error processing image {image}: {e}", exc_info=True)
        raise

def format_student_info(response):
    """
    Formats student information for CSV output.

    Args:
        response (dict): The response from DynamoDB scan.

    Returns:
        list: A list containing student information.
    """
    try:
        student_info = []
        for student_item in response['Items']:
            name = student_item['name']['S']
            major = student_item['major']['S']
            year = student_item['year']['S']
            student_info.append([name, major, year])
        return student_info
    except Exception as e:
        logging.error(f"Error formatting student information: {e}", exc_info=True)
        raise
def upload_csv(student_info, frame_file):
    """
    Uploads CSV file to S3 bucket.

    Args:
        student_info (list): A list containing student information.
        frame_file (str): The name of the frame file.
    """
    try:
        video_basename = os.path.splitext(frame_file)[0].rsplit('_', 1)[0]  # Remove '_frame' suffix
        csv_filename = f'{video_basename}.csv'
        csv_content = '\n'.join([','.join(row) for row in student_info])
        s3.put_object(
            Bucket=OUTPUT_BUCKET_NAME,
            Key=csv_filename,
            Body=csv_content
        )
    except Exception as e:
        logging.error(f"Error uploading CSV for {frame_file}: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    result = face_recognition_handler()
    print(result)
