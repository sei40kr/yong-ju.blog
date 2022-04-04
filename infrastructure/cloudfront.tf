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
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  origin {
    domain_name = aws_s3_bucket.blog.website_endpoint
    origin_id   = "s3"

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["SSLv3"]
    }
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
