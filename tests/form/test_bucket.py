import os, base64
from packages.vision.store.bucket import Bucket

def test_bucket_write_read():
    bucket_args = {
        "S3_HOST": os.getenv("S3_HOST"),
        "S3_PORT": os.getenv("S3_PORT"),
        "S3_ACCESS_KEY": os.getenv("S3_ACCESS_KEY"),
        "S3_SECRET_KEY": os.getenv("S3_SECRET_KEY"),
        "S3_BUCKET_DATA": os.getenv("S3_BUCKET_DATA"),
        "S3_API_URL": os.getenv("S3_API_URL"),
    }
    bucket = Bucket(bucket_args)
    test_key = "test/testfile.txt"
    test_data = b"hello world"

    wr = bucket.write(test_key, test_data)
    print("Write result:", wr)

    data = bucket.read(test_key)
    print("Read data:", data)

    assert data == test_data, "Data read is different from data written"

if __name__ == "__main__":
    test_bucket_write_read()
