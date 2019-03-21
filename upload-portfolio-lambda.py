import json
import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    sns = boto3.resource('sns')
    topic = sns.Topic('arn:aws:sns:us-east-1:636506077101:deployPortfolioTopic')

    try:
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

      print "Job done!"
      topic.publish(Subject='Portfolio Deployment Success', Message='Deployment for portfolio was successful.')

    except:
      topic.publish(Subject='Portfolio Deployment Failed', Message='Deployment for portfolio was not successful.')
      raise

    return { 'status': 'completed' }
