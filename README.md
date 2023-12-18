# EduCloud: Hybrid Cloud-Based Smart Classroom Assistant

## Description
"EduCloud" is a cloud-based application designed for smart classroom assistance. It combines AWS, Ceph, and OpenFaaS in a hybrid cloud setup, emphasizing scalability, cost-effectiveness, and dynamic resource allocation.

## Installation

### OpenFaaS Setup
- Install Minikube, faas-cli, and helm.
- Deploy OpenFaaS on a local Kubernetes cluster.

### Ceph Setup
- Set up a Ceph storage cluster and Ceph RGW for object storage.
- Configure Ceph as an alternative to AWS S3.

### AWS and Environment Configuration
- Set up AWS Lambda functions, S3 buckets, and DynamoDB.

## Running the Application
- Triggered by video uploads to the Ceph RGW input bucket.
- AWS Lambda processes videos for face recognition and academic data retrieval.
- Output is stored in the Ceph RGW output bucket and monitored via the local VM's CLI.

## Testing
- Use `workload.py` for comprehensive testing.
- Check face recognition accuracy and input/output data handling.

## Additional Information
- For detailed architecture, tasks, and evaluation, refer to the [CSE 546 Project Report 3](file-s2ele6G9SmuiOHcx28AQPS0m).
