resource "aws_kms_key" "guardduty_data_encryption" {
  description             = "KMS key for tranfering guardduty logs into s3"
  deletion_window_in_days = 10
  is_enabled = true
  multi_region = true
  key_usage = "ENCRYPT_DECRYPT"
  
  # customer_master_key_spec = Defaults to SYMMETRIC_DEFAULT
  # key_usage = Defaults to ENCRYPT_DECRYPT
}