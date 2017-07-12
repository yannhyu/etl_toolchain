#!/usr/bin/perl
use strict;
use warnings;

my %personal_info = (
    "Cleaver", {
        "FIRST",  "Ward",
        "SPOUSE", "June",
    },
    "Flintstone", {
        "FIRST",  "Fred",
        "SPOUSE", "Wilma",
    },
    "Bunker", {
        "FIRST",  "Archie",
        "SPOUSE", "Edith",
    },
);

print "Fred's wife is $personal_info{Flintstone}->{SPOUSE}\n";

# the arrow is option in this case
print "Fred's wife is $personal_info{Flintstone}{SPOUSE}\n";
 
my $bunker = $personal_info{Bunker};
# my $bunker = $personal_info{"Bunker"};
print "Bunker's wife is $bunker->{SPOUSE}\n";