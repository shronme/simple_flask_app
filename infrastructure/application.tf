# resource "aws_elastic_beanstalk_application" "cf-eb" {
#     name        = "cf-eb-app"
#     description = "eb for cf app"
# }

# resource "aws_elastic_beanstalk_environment" "cf-eb-test" {
#     name = "cf-eb-test"
#     application = "cf-eb-app"
#     solution_stack_name = "64bit Amazon Linux 2018.03 v2.20.0 running Multi-container Docker 18.09.9-ce (Generic)"
    
#     setting {
#         namespace = "aws:autoscaling:launchconfiguration"
#         name = "IamInstanceProfile"
#         value = aws_iam_instance_profile.ec2.name
#     }

#     setting {
#         namespace = "aws:ec2:vpc"
#         name = "VPCId"
#         value = aws_vpc.app-vpc.id
#     }

#     setting {
#         namespace = "aws:ec2:vpc"
#         name = "Subnets"
#         value = join(",", aws_subnet.private_subnet.*.id)
#     }

#     setting {
#         namespace = "aws:ec2:vpc"
#         name = "ELBSubnets"
#         value = join(",", aws_subnet.public_subnet.*.id)
#     }

#     setting {
#         namespace = "aws:ec2:vpc"
#         name = "ELBScheme"
#         value = "internal"
#     }
  
#     setting {
#         namespace = "aws:autoscaling:launchconfiguration"
#         name = "InstanceType"
#         value = "t2.micro"
#     }
#     setting {
#         namespace = "aws:autoscaling:asg"
#         name = "Availability Zones"
#         value = "Any 2"
#     }
  
#     setting {
#         namespace = "aws:autoscaling:asg"
#         name = "MinSize"
#         value = "1"
#     }
  
#     setting {
#         namespace = "aws:autoscaling:asg"
#         name = "MaxSize"
#         value = "2"
#     }

# }
