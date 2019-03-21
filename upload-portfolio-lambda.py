import json
import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):

    # setup s3 resource
    s3 = boto3.resource('s3')
    # get portfolio bucket and the build
    portfolio_bucket = s3.Bucket('portfolio.kaylarwebb')
    build_bucket = s3.Bucket('portfoliobuild.kaylarwebb')

    # create in memory file
    portfolio_zip = StringIO.StringIO()
    # download bucket object from s3 and set it to in memory file
    build_bucket.download_fileobj('webbportfolio.zip', portfolio_zip)

    # extract, upload and set the acl
    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm)
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
    }
