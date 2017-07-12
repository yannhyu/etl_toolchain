#!/usr/bin/perl
use strict;
use warnings;

my %last_name_hash = (
  "Ward",   "Cleaver",
  "Fred",   "Flintstone",
  "Archie", "Bunker"
);

print "Archie $last_name_hash{Archie}\n";

print "Archie $last_name_hash{Fred}\n";

my $x = $last_name_hash{"Ward"};
print "\$found is now ", $x, " \n";