vpc = {
  cidr = "10.0.0.0/16"
  name = "cf-vpc"
  ig_name = "cf-VpcInternetGateway"
  s3_endpoint_name = "cf-VpcS3Endpoint"
  public_subnets_routetable_name = "cf-VpcPublicSubnetRouteTable"
  default_route_table_name = "cf-VpcMainRouteTable"

  azs = [ 
    { 
      az = "eu-west-1a"
      public_subnet = {
    	  cidr = "10.0.1.0/24"
    	  name = "cf-1APublicSubnet"
    	  nat_name = "cf-1APublicSubnetNatGateway"
    	  nat_eip_name = "cf-1APublicSubnetNatGatewayEip"
      }
      private_subnet = {
      	cidr = "10.0.0.0/24"
      	name = "cf-1APrivateSubnet"
      	routetable_name = "cf-1APrivateRouteTable"
      }
    },
    { 
      az = "eu-west-1b"
      public_subnet = {
    	  cidr = "10.0.2.0/24"
    	  name = "cf-1BPublicSubnet"
    	  nat_name = "cf-1BPublicSubnetNatGateway"
    	  nat_eip_name = "cf-1BPublicSubnetNatGatewayEip"
      }
      private_subnet = {
      	cidr = "10.0.3.0/24"
      	name = "cf-1BPrivateSubnet"
      	routetable_name = "cf-1BPrivateRouteTable"
      }
    },
    { 
      az = "eu-west-1c"
      public_subnet = {
    	  cidr = "10.0.4.0/24"
    	  name = "cf-1CPublicSubnet"
    	  nat_name = "cf-1BPublicSubnetNatGateway"
    	  nat_eip_name = "cf-1CPublicSubnetNatGatewayEip"
      }
      private_subnet = {
      	cidr = "10.0.5.0/24"
      	name = "cf-1CPrivateSubnet"
      	routetable_name = "cf-1CPrivateRouteTable"
      }
    }
  ]
}