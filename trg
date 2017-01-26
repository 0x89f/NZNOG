
RP/0/0/CPU0:tauranga#sh run
Wed Jan 25 18:29:10.632 UTC
Building configuration...
!! IOS XR Configuration 6.0.0
!! Last configuration change at Wed Jan 25 08:12:11 2017 by cisco
!
hostname tauranga
domain name core.net
ipv4 unnumbered mpls traffic-eng Loopback0
interface Loopback0
 ipv4 address 10.1.1.5 255.255.255.255
!
interface MgmtEth0/0/CPU0/0
 shutdown
!
interface GigabitEthernet0/0/0/0
 ipv4 address 192.168.15.1 255.255.255.254
!
interface GigabitEthernet0/0/0/1
 ipv4 address 192.168.45.1 255.255.255.254
!
interface GigabitEthernet0/0/0/2
 shutdown
!
interface GigabitEthernet0/0/0/3
 shutdown
!
interface GigabitEthernet0/0/0/4
 shutdown
!
interface GigabitEthernet0/0/0/5
 shutdown
!
interface GigabitEthernet0/0/0/6
 shutdown
!
router isis core
 is-type level-1
 net 49.2222.1234.1234.0005.00
 distribute bgp-ls level 1
 address-family ipv4 unicast
  metric-style wide
  mpls traffic-eng level-1
  mpls traffic-eng router-id Loopback0
 !
 interface Loopback0
  address-family ipv4 unicast
  !
 !
 interface GigabitEthernet0/0/0/0
  point-to-point
  address-family ipv4 unicast
  !
 !
 interface GigabitEthernet0/0/0/1
  point-to-point
  address-family ipv4 unicast
  !
 !
!
rsvp
 interface Loopback0
 !
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/1
 !
!
mpls traffic-eng
 interface GigabitEthernet0/0/0/0
 !
 interface GigabitEthernet0/0/0/1
 !
 pce
  peer ipv4 192.168.100.130
  !
  stateful-client
   instantiation
   cisco-extension
   report
  !
 !
 auto-tunnel pcc
  tunnel-id min 1001 max 1099
 !
!
ssh server v2
ssh server vrf default
ssh server netconf vrf default
ssh timeout 120
netconf-yang agent
 ssh
!
end

RP/0/0/CPU0:tauranga#   
