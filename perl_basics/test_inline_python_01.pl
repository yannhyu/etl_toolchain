#!/usr/bin/perl
# use strict;
use warnings;
use Inline Python;

my $SOME_NAME = "Dr. Juan Q. Xavier de la Vega III (Doc Vega)";

my $fname = get_fname($SOME_NAME);
print "First name is $fname\n";

my @PEOPLE_NAMES = (
        "Adriana C. Ocampo Uria",
        "Albert Einstein",
        "Anna K. Behrensmeyer",
        "Blaise Pascal",
        "Caroline Herschel",
        "Cecilia Payne-Gaposchkin",
        "Chien-Shiung Wu",
        "Dorothy Hodgkin",
        "Edmond Halley",
        "Edwin Powell Hubble",
        "Elizabeth Blackburn",
        "Enrico Fermi",
        "Erwin Schroedinger",
        "Flossie Wong-Staal",
        "Frieda Robscheit-Robbins",
        "Geraldine Seydoux",
        "Gertrude B. Elion",
        "Ingrid Daubechies",
        "Jacqueline K. Barton",
        "Jane Goodall",
        "Jocelyn Bell Burnell",
        "Johannes Kepler",
        "Lene Vestergaard Hau",
        "Lise Meitner",
        "Lord Kelvin",
        "Maria Mitchell",
        "Marie Curie",
        "Max Born",
        "Max Planck",
        "Melissa Franklin",
        "Michael Faraday",
        "Mildred S. Dresselhaus",
        "Nicolaus Copernicus",
        "Niels Bohr",
        "Patricia S. Goldman-Rakic",
        "Patty Jo Watson",
        "Polly Matzinger",
        "Richard Phillips Feynman",
        "Rita Levi-Montalcini",
        "Rosalind Franklin",
        "Ruzena Bajcsy",
        "Sarah Boysen",
        "Shannon W. Lucid",
        "Shirley Ann Jackson",
        "Sir Ernest Rutherford",
        "Sir Isaac Newton",
        "Stephen Hawking",
        "Werner Karl Heisenberg",
        "Wilhelm Conrad Roentgen",
        "Wolfgang Ernst Pauli",
    );

for my $name (@PEOPLE_NAMES) 
{
    print "First name is ", get_fname($name), "; middle name is ", get_mname($name), "\n";
}

__END__
__Python__

from mlxlibrary import get_fname, get_mname