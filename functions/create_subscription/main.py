import os
import json
import uuid
import time

import boto3
import jwt

def generate_subscription(email):
  subscription_id = uuid.uuid4().hex
  subscription = {
      'pk': subscription_id,
      'sk': subscription_id,
      'verified': False,
      'email': email
  }
  return subscription

def generate_token(subscription, verification):
  payload = {
    'subscription': subscription['pk'],
    'verification': verification['sk']
  }
  token = jwt.encode(
    payload,
    verification['secret'],
    algorithm='HS256'
  )
  return token

def generate_verification(subscription_id):
  signing_secret = uuid.uuid4().hex
  raw_verification_id = uuid.uuid4().hex
  verification_id = f'verification#{raw_verification_id})'
  ttl = 259200 + time.time() # 3 days
  verification = {
    'pk': subscription_id,
    'sk': verification_id,
    'active': True,
    'ttl': ttl,
    'secret': signing_secret
  }
  return verification

def send_verification_email(to_addresses, data, from_address=''):
  template_name = os.environ['TEMPLATE_NAME']
  ses = boto3.client('ses')
  return ses.send_templated_email(
    Source=from_address,
    Destination={
      'ToAddresses': to_addresses,
    },
    Template=template_name,
    TemplateData=json.dumps(data)
  )

def handler(event, ctx=None):
  table_name = os.environ['TABLE_NAME']
  body = json.loads(event['body'])
  email = body['email']

  client = boto3.resource('dynamodb')
  table = client.Table(table_name)

  # Create Subscription
  subscription = generate_subscription(email)
  table.put_item(Item=subscription)

  # Create Verification
  verification = generate_verification(subscription['pk'])
  table.put_item(Item=verification)

  # Create Token
  token = generate_token(subscription, verification)

  send_verification_email(
    to_addresses=[email],
    data={
      'token': token
    }
  )
