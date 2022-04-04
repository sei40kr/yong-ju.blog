data "aws_iam_policy_document" "blog" {
  statement {
    sid       = "PublicReadGetObject"
    actions   = ["s3:GetObject"]
    resources = ["${aws_s3_bucket.blog.arn}/*"]

    principals {
      type        = "*"
      identifiers = ["*"]
    }
  }
}

resource "aws_s3_bucket" "blog" {
  bucket = "yong-ju.blog"
  tags   = {
    Owner = "blog"
  }
}

resource "aws_s3_bucket_policy" "blog" {
  bucket = aws_s3_bucket.blog.id
  policy = data.aws_iam_policy_document.blog.json
}

resource "aws_s3_bucket_website_configuration" "blog" {
  bucket = aws_s3_bucket.blog.bucket

  index_document {
    suffix = "index.html"
  }
}
