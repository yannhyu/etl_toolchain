#!/usr/bin/perl
use strict;
use warnings;

my $never_set;
my $numeric_zero = 0.00;
my $numeric_one = 1;
my $string_zero = "0";
my $string_one = "1";
my $string_float_zero = "0.00";

unless ( $never_set )
{
    print "\$never_set is false\n";
}

unless ( $numeric_zero )
{
    print "\$numeric_zero is false\n";
}

unless ( $numeric_one )
{
    print "\$numeric_one is false\n";
}

unless ( $string_zero )
{
    print "\$string_zero is false\n";
}

unless ( $string_one )
{
    print "\$string_one is false\n";
}

unless ( $string_float_zero )
{
    print "\$string_float_zero is false\n";
}