from flask import Flask, request
import handler_Test as handler  # Import your Handler_Test script

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Data received:", data)

    # Extract bucket and key from the received data
    bucket = data.get('bucket')
    key = data.get('key')

    if bucket and key:
        # Call the handler function with the bucket and key
        result = handler.face_recognition_handler(bucket, key)
        print("Handler result:", result)
    else:
        print("No bucket or key in the received data")

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
