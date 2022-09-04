data "aws_iam_policy_document" "allow_cloudfront_service_principal_readonly" {
  statement {
    sid = "AllowCloudFrontServicePrincipalReadOnly"

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    actions = ["s3:GetObject"]

    resources = ["${aws_s3_bucket.blog.arn}/*"]

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [aws_cloudfront_distribution.blog.arn]
    }
  }
}

resource "aws_iam_user" "blog" {
  name = "blog"
  tags = { Project = "yong-ju.blog" }
}

resource "aws_iam_access_key" "blog" {
  user = aws_iam_user.blog.name
}
