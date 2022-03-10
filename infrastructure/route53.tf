resource "aws_route53_record" "blog_ipv4" {
  name    = "blog.yong-ju.me"
  type    = "A"
  zone_id = data.aws_route53_zone.yong_ju_me.zone_id

  alias {
    name                   = aws_cloudfront_distribution.blog.domain_name
    evaluate_target_health = false
    zone_id                = aws_cloudfront_distribution.blog.hosted_zone_id
  }
}

resource "aws_route53_record" "blog_ipv6" {
  name    = "blog.yong-ju.me"
  type    = "AAAA"
  zone_id = data.aws_route53_zone.yong_ju_me.zone_id

  alias {
    name                   = aws_cloudfront_distribution.blog.domain_name
    evaluate_target_health = false
    zone_id                = aws_cloudfront_distribution.blog.hosted_zone_id
  }
}
