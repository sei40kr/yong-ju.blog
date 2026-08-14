# Monthly cost alert for the blog.

# The budget below filters on Project, which Cost Explorer only reports on once
# the tag is an *active* cost allocation tag — otherwise every tagged cost is
# invisible and the budget sits at $0. Activation applies to cost from the
# activation month onward only; reaching further back needs the console's
# backfill.
resource "aws_ce_cost_allocation_tag" "project" {
  tag_key = "Project"
  status  = "Active"
}

variable "monthly_budget_usd" {
  description = "Monthly cost ceiling for the blog. USD is the only unit this account's billing supports, so this is a round dollar figure rather than a converted yen one -- USD 3 was about JPY 480 at 159 JPY/USD in August 2026."
  type        = string
  default     = "3"
}

variable "budget_notification_email" {
  description = "Address that receives the budget alerts."
  type        = string
  default     = "sei40kr@gmail.com"
}

resource "aws_budgets_budget" "blog" {
  name              = "blog"
  budget_type       = "COST"
  limit_amount      = var.monthly_budget_usd
  limit_unit        = "USD"
  time_unit         = "MONTHLY"
  time_period_start = "2026-08-01_00:00"

  cost_filter {
    name   = "TagKeyValue"
    values = [format("Project$%s", local.project_tag)]
  }

  # The "about to go over" alert: AWS projects the month-end total and fires
  # before it actually lands. Needs ~5 weeks of history before it can forecast.
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "FORECASTED"
    subscriber_email_addresses = [var.budget_notification_email]
  }

  # Backstop for what the forecast misses: no history yet, or a spike late
  # enough in the month that the forecast never caught up.
  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 100
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.budget_notification_email]
  }
}
