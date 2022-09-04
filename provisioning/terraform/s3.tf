resource "aws_s3_bucket" "blog" {
  bucket = "yong-ju.blog"
  tags   = {
    Owner = "blog"
  }
}

resource "aws_s3_bucket_acl" "blog" {
  bucket = aws_s3_bucket.blog.id
  acl    = "private"
}

resource "aws_s3_bucket_policy" "allow_cloudfront_service_principal_readonly" {
  bucket = aws_s3_bucket.blog.id
  policy = data.aws_iam_policy_document.allow_cloudfront_service_principal_readonly.json
}
