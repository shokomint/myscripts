#!/usr/bin/perl
#
#open(FH,$1);
#@data = <FH>;
#close(FH);

#open(FH,"> $ARGV[0]");
#


$str = &conv2seireki("あいえうお平成二十九年あいうえお");
#$str = &conv2seireki("あいえうお昭和一年あいうえお");
print $str;
print "\n";
sub conv2seireki {
    my $str = @_[0];
    $str =~ /(昭和|平成)([一二三四五六七八九十]+)年/;
    my $type = $1;
    my $year = &conv2number($2);

    if($type eq "昭和") {
        $year = $year + 1925;
    } elsif($type eq "平成") {
        $year = $year + 1988;
    }

    $bef =~ /[一二三四五六七八九十]+月/;
    my $month = &conv2number($1);

    $bef =~/[一二三四五六七八九十]+日/;
    my $day = &conv2number($1);

    $str =~ s/(昭和|平成)[一二三四五六七八九十]+年/$year\//;
    $str =~ s/[一二三四五六七八九十]+月/$monthu\//;
    $str =~ s/[一二三四五六七八九十]+日/$day/;

    if($year == 0 && $month == 0 && $day == 0) {
        return "";
    } else {
        return $str;
    }
}

sub conv2number {
    my $x = @_[0];
    $x =~ s/^十/1/;
    $x =~ s/一/1/g;
    $x =~ s/二/2/g;
    $x =~ s/三/3/g;
    $x =~ s/四/4/g;
    $x =~ s/五/5/g;
    $x =~ s/六/6/g;
    $x =~ s/七/7/g;
    $x =~ s/八/8/g;
    $x =~ s/九/9/g;
    $x =~ s/十//g;
    return($x);
}
#close(FH)
