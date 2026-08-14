terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }

  backend "s3" {
    bucket = "yong-ju.blog-tfstate"
    key    = "terraform.tfstate"
    region = "ap-northeast-1"
  }
}

# Tag applied to every taggable resource here, via the providers' default_tags.
# Also the cost allocation tag the budget in budgets.tf filters on, so the two
# can never drift apart.
locals {
  project_tag = "yong-ju.blog"
}

provider "aws" {
  region = "ap-northeast-1"

  default_tags {
    tags = { Project = local.project_tag }
  }
}

provider "aws" {
  alias  = "us_east_1"
  region = "us-east-1"

  default_tags {
    tags = { Project = local.project_tag }
  }
}

data "aws_route53_zone" "yong_ju_blog" {
  name = "yong-ju.blog"
}
