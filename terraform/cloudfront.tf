resource "aws_cloudfront_distribution" "blog" {
  aliases             = ["yong-ju.blog"]
  default_root_object = "index.html"
  enabled             = true
  is_ipv6_enabled     = true
  tags                = {
    Owner = "blog"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "s3"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.url_rewrite.arn
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  origin {
    domain_name = aws_s3_bucket.blog.bucket_regional_domain_name
    origin_id   = "s3"

    origin_access_control_id = aws_cloudfront_origin_access_control.blog.id
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate.blog.arn
    minimum_protocol_version = "TLSv1"
    ssl_support_method       = "sni-only"
  }
}

resource "aws_cloudfront_function" "url_rewrite" {
  name    = "url-rewrite"
  code    = file("${path.module}/url-rewrite.js")
  runtime = "cloudfront-js-1.0"
}

resource "aws_cloudfront_origin_access_control" "blog" {
  name                              = "yong-ju.blog"
  description                       = ""
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}
