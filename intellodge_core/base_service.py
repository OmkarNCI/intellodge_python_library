from botocore.exceptions import ClientError
import boto3
from .logger import get_logger

logger = get_logger(__name__)

class BaseDynamoDBService:
    def __init__(self, table_name, region_name="us-east-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)
        self.logger = get_logger(f"intellodge.{table_name}")

    def create(self, item):
        try:
            self.table.put_item(Item=item)
            logger.info(f"Created item: {item}")
            return {"success": True, "item": item}
        except ClientError as e:
            logger.error(f"Create failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def read(self, key):
        try:
            response = self.table.get_item(Key=key)
            item = response.get("Item")
            logger.info(f"Fetching item: {item} with key {key}")
            return {"success": True, "item": item}
        except ClientError as e:
            logger.error(f"Fetching item failed: {str(e)}")
            return {"success": False, "error": str(e)}

    def update(self, key, updates):
        update_expr = "SET " + ", ".join([f"{k}=:{k}" for k in updates])
        expr_vals = {f":{k}": v for k, v in updates.items()}
        try:
            self.table.update_item(
                Key=key,
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_vals,
            )
            logger.info(f"Updated key: {key} with updates {updates}")
            return {"success": True, "updated_fields": updates}
        except Exception as e:
            logger.error(f"Update failed: {key}: {str(e)}")
            return {"success": False, "error": str(e)}

    def delete(self, key):
        try:
            self.table.delete_item(Key=key)
            logger.info(f"Deleted item with key {key}")
            return {"success": True}
        except ClientError as e:
            logger.error(f"Delete failed: {str(e)}")
            return {"success": False, "error": str(e)}
