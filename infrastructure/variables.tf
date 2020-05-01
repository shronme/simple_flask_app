variable "vpc" {
  type = object({
    cidr = string
    name = string
    ig_name = string
    s3_endpoint_name = string
    public_subnets_routetable_name = string
    default_route_table_name = string
    azs = list(object({
      az = string
      public_subnet = object({
        cidr = string
        name = string
        nat_name = string
        nat_eip_name = string
      })
      private_subnet = object({
        cidr = string
        name = string
        routetable_name = string
      })
    }))   
  })
}
