#!/usr/bin/perl
#
#open(FH,$1);
@data = <FH>;
#close(FH);

#open(FH,"> $ARGV[0]");

foreach my $d @data {

    
   $tmp = &conv2seireki()     
}
$str = &conv2seireki("一 百二十一条一項あ一日いえうおいうえお");
$str = &convTitleNumber($str);
$str = &convRuleNumber($str);
print $str;
#print $str;
#print "\n";

#close(FH);

sub convRuleNumber {
    my $str = @_[0];
    $str =~ /([一二三四五六七八九十百]+)条/;
    my $jyo = $1;
    if($jyo) {
        $jyo = &conv2number($jyo);
        $str =~ s/([〇一二三四五六七八九十百]+条)/$jyo条/;
     }

    $str =~ /([一二三四五六七八九十百]+)項/;
    $kou = $1;
    if($kou) {
        my $kou = &conv2number($kou);
        $str =~ s/([〇一二三四五六七八九十百]+項)/$kou項/;
    }
    return($str);
}

     
sub convTitleNumber {
    my $str = @_[0];
    $str =~ s/^一/１．/;
    $str =~ s/^二/２．/;
    $str =~ s/^三/３．/;
    $str =~ s/^四/４．/;
    $str =~ s/^五/５．/;
    $str =~ s/^六/６．/;
    $str =~ s/^七/７．/;
    $str =~ s/^八/８．/;
    $str =~ s/^九/９．/;
    $str =~ s/^十$/１０．/;
    $str =~ s/^十一/１１．/;
    $str =~ s/^十二/１２．/;
    return($str);
}
sub conv2seireki {
    my $str = @_[0];
    $str =~ /(昭和|平成)([〇一二三四五六七八九十]+)年/;
    my $type = $1;
    my $year = &conv2number($2);

    if($type eq "昭和") {
        $year = $year + 1925;
    } elsif($type eq "平成") {
        $year = $year + 1988;
    }

    if($year == 0) {
        $str =~/([〇一二三四五六七八九十]+)年/;
        $year = &conv2number($1);
    }

    $str =~ /([〇一二三四五六七八九十]+)月/;
    my $month = &conv2number($1);

    $str =~/([一二三四五六七八九十]+)日/;
    my $day = &conv2number($1);

    if($year > 0 && $month > 0) {
        $str =~ s/(昭和|平成)[〇一二三四五六七八九十]+年/$year\//;
        $str =~ s/[〇一二三四五六七八九十]+年/$year\//;
        $str =~ s/[〇一二三四五六七八九十]+月/$month\//;
        $str =~ s/[〇一二三四五六七八九十]+日/$day/;
    } elsif($month > 0 && $day > 0) {
        $str =~ s/[〇一二三四五六七八九十]+月/$month\//;
        $str =~ s/[〇一二三四五六七八九十]+日/$day/;
    }

    if($year > 0 && $month == 0 && $day == 0) {
        $str =~ s/[〇一二三四五六七八九十]+年/$year年/;
    } elsif($month > 0 && $year == 0 && $day == 0) {
        $str =~ s/[〇一二三四五六七八九十]+月/$month月/;
    } elsif($day > 0 && $year == 0 && $month == 0) {
        $str =~ s/[〇一二三四五六七八九十]+日/$day日/;
    }

    $str =~ s/\/(\D+)/$1/;

    return $str;
}

sub conv2number {
    my $x = @_[0];

    $x =~ /^([〇一二三四五六七八九十百]+)$/;
    if(!$1) {
        return(0);
    }

    $x =~ s/^(百)([一二三四五六七八九十]+)/1${2}/;
    $x =~ s/([一二三四五六七八九十]+)(百)$/${1}00/;
    $x =~ s/([一二三四五六七八九十]+)(百)([一二三四五六七八九十]+)/${1}0${3}/;
    $x =~ s/^(百)$/100/;

    $x =~ s/^(十)([一二三四五六七八九]+)/1$2/;
    $x =~ s/([一二三四五六七八九]+)十$/${1}0/;
    $x =~ s/([一二三四五六七八九]+)(十)([一二三四五六七八九]+)/${1}${3}/;
    $x =~ s/^十$/10/;

    $x =~ s/十/1/;
    $x =~ s/百/1/;
    $x =~ s/〇/0/g;
    $x =~ s/一/1/g;
    $x =~ s/二/2/g;
    $x =~ s/三/3/g;
    $x =~ s/四/4/g;
    $x =~ s/五/5/g;
    $x =~ s/六/6/g;
    $x =~ s/七/7/g;
    $x =~ s/八/8/g;
    $x =~ s/九/9/g;
    return($x);
}
