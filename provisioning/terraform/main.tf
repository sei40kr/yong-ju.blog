terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

provider "aws" {
  region = "ap-northeast-1"
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"
}

data "aws_route53_zone" "yong_ju_blog" {
  name = "yong-ju.blog"
}
