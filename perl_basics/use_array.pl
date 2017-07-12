#!/usr/bin/perl
use strict;
use warnings;

my @last_name = (
  "Ward",   "Cleaver",
  "Fred",   "Flintstone",
  "Archie", "Bunker"
);

# if we want to know Archie's last name
# we have to do a linear search
my $lname;
for (my $i = 0; $i < @last_name; $i += 2) {
  $lname = $last_name[$i+1] if $last_name[$i] eq "Archie";
}
print "Archie $lname\n";