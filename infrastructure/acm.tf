resource "aws_acm_certificate" "blog" {
  domain_name       = "yong-ju.blog"
  provider          = aws.us_east_1
  validation_method = "DNS"
  tags              = {
    Owner = "blog"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "blog" {
  certificate_arn         = aws_acm_certificate.blog.arn
  provider                = aws.us_east_1
  validation_record_fqdns = [for record in aws_route53_record.blog_validation : record.fqdn]
}

resource "aws_route53_record" "blog_validation" {
  for_each = {
  for dvo in aws_acm_certificate.blog.domain_validation_options : dvo.domain_name => {
    name   = dvo.resource_record_name
    record = dvo.resource_record_value
    type   = dvo.resource_record_type
  }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.yong_ju_blog.zone_id
}
