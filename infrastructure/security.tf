# #
# # EC2
# #
# data "aws_iam_policy_document" "ec2" {
#   statement {
#     sid = ""

#     actions = [
#       "sts:AssumeRole",
#     ]

#     principals {
#       type        = "Service"
#       identifiers = ["ec2.amazonaws.com"]
#     }

#     effect = "Allow"
#   }

#   statement {
#     sid = ""

#     actions = [
#       "sts:AssumeRole",
#     ]

#     principals {
#       type        = "Service"
#       identifiers = ["ssm.amazonaws.com"]
#     }

#     effect = "Allow"
#   }
# }

# resource "aws_iam_role" "ec2" {
#     name               = "cf-app-eb-ec2"
#     assume_role_policy = data.aws_iam_policy_document.ec2.json
# }

# resource "aws_iam_instance_profile" "ec2" {
#     name = "cf-app-eb-ec2-profile"
#     role = aws_iam_role.ec2.name

# }

