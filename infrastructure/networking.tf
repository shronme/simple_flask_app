resource "aws_vpc" "app-vpc" {
    assign_generated_ipv6_cidr_block = false
    cidr_block                       = var.vpc.cidr
    enable_classiclink               = false
    enable_classiclink_dns_support   = false
    enable_dns_hostnames             = true
    enable_dns_support               = true
    instance_tenancy                 = "default"
    tags = {
        Name = var.vpc.name
    }
  
}

data "aws_region" "current" {
  #provider = "aws.region"
}

resource "aws_internet_gateway" "app-ig" {
  vpc_id = aws_vpc.app-vpc.id
  tags = {
    Name = var.vpc.ig_name
  }
}

resource "aws_vpc_endpoint" "app-vpc-ep" {
  vpc_id       = aws_vpc.app-vpc.id
  service_name = format("com.amazonaws.%s.s3", data.aws_region.current.name)
  tags = {
    Name = var.vpc.s3_endpoint_name
  }
}

resource "aws_subnet" "public_subnet" {
  count      = length(var.vpc.azs)
  cidr_block = var.vpc.azs[count.index].public_subnet.cidr
  vpc_id     = aws_vpc.app-vpc.id

  map_public_ip_on_launch = true
  availability_zone       = var.vpc.azs[count.index].az

  tags = {
    Name = var.vpc.azs[count.index].public_subnet.name
  }
}

resource "aws_subnet" "private_subnet" {
  count      = length(var.vpc.azs)
  cidr_block = var.vpc.azs[count.index].private_subnet.cidr
  vpc_id     = aws_vpc.app-vpc.id

  map_public_ip_on_launch = false
  availability_zone       = var.vpc.azs[count.index].az

  tags = {
    Name = var.vpc.azs[count.index].private_subnet.name
  }
}

resource "aws_eip" "public_subnet_nat_eip" {
  count      = length(var.vpc.azs)
  vpc  = true
  tags = { 
    Name = var.vpc.azs[count.index].public_subnet.nat_eip_name
  }
}

resource "aws_nat_gateway" "public_subnet_nat" {
  count      = length(var.vpc.azs)
  subnet_id     = aws_subnet.public_subnet[count.index].id
  allocation_id = aws_eip.public_subnet_nat_eip[count.index].id
  #depends_on    = [aws_internet_gateway.app-ig[count.]
  tags = {
    Name = var.vpc.azs[count.index].public_subnet.nat_name
  }
}

resource "aws_route_table" "public_subnet_route_table" {
  vpc_id = aws_vpc.app-vpc.id
  route = [
    {
      cidr_block                = "0.0.0.0/0"
      gateway_id                = aws_internet_gateway.app-ig.id
      nat_gateway_id            = ""
      ipv6_cidr_block           = ""
      egress_only_gateway_id    = ""
      instance_id               = ""
      network_interface_id      = ""
      transit_gateway_id        = ""
      vpc_peering_connection_id = ""
    },
  ]
  tags = {
    Name = var.vpc.public_subnets_routetable_name
  }
}

resource "aws_route_table" "private_subnet_route_table" {
  count      = length(var.vpc.azs)
  vpc_id = aws_vpc.app-vpc.id
  route = [
    {
      cidr_block                = "0.0.0.0/0"
      nat_gateway_id            = aws_nat_gateway.public_subnet_nat[count.index].id
      gateway_id                = ""
      ipv6_cidr_block           = ""
      egress_only_gateway_id    = ""
      instance_id               = ""
      network_interface_id      = ""
      transit_gateway_id        = ""
      vpc_peering_connection_id = ""
    },
  ]
  tags = {
    Name = var.vpc.azs[count.index].private_subnet.routetable_name
  }
}

resource "aws_route_table_association" "public_route_table_public_subnet_association" {
  count      = length(var.vpc.azs)
  subnet_id      = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.public_subnet_route_table.id
}

resource "aws_route_table_association" "private_route_table_private_subnet_association" {
  count      = length(var.vpc.azs)
  subnet_id      = aws_subnet.private_subnet[count.index].id
  route_table_id = aws_route_table.private_subnet_route_table[count.index].id
}

resource "aws_default_route_table" "app-def-rt" {
  default_route_table_id = aws_vpc.app-vpc.default_route_table_id
  tags = {
    Name = var.vpc.default_route_table_name
  }
}


