#!/usr/bin/perl -w
use utf8;
use Encode;
use warnings;
use open IN  => ":utf8";
use open OUT  => ":utf8";
binmode STDIN,  ":utf8";
binmode STDOUT, ":utf8";
binmode STDERR, ":utf8";
use Data::Dumper;
use Test::More 'no_plan';

if($ARGV[0] eq "--test") {
    my @data = (
        {"test"=>"百十五","expected"=>115},
        {"test"=>"九十五","expected"=>95},
        {"test"=>"二〇十七","expected"=>2017},
        {"test"=>"二〇一七","expected"=>2017},
        {"test"=>"二〇〇七","expected"=>2007},
        {"test"=>"二百十八","expected"=>218},
        {"test"=>"二百二十八","expected"=>228},
        {"test"=>"百二十八","expected"=>128},
        {"test"=>"二十九","expected"=>29},
        {"test"=>"二十一","expected"=>21},
        {"test"=>"二百一","expected"=>201},
        {"test"=>"二〇一","expected"=>201},
    );

    foreach my $d (@data) {
        is(&conv2number($d->{test}),$d->{expected},encode("utf-8",$d->{test}));
    }

} else {
    &mymain();
}
    

sub mymain() {
    open(FH,$ARGV[0]);
    my @data = <FH>;
    close(FH);

    open(FH,"> $ARGV[0]");

    foreach my $d (@data) {
    
        $tmp = $d;
        while($tmp =~ /[〇一二三四五六七八九十百]+[条|項|号|月|年|日]/) {
            $tmp = &conv2seireki($tmp);
            $tmp = &convRuleNumber($tmp);
        }
        $tmp = &convTitleNumber($tmp);
        print FH $tmp;
    }

    close(FH);
}

sub convRuleNumber {
    my $str = $_[0];
    if($str =~ /([一二三四五六七八九十百]+)条/) {
        my $jyo = $1;
        $jyo = &conv2number($jyo);
        $str =~ s/([〇一二三四五六七八九十百]+条)/${jyo}条/;
        return($str);
     }

    if($str =~ /([一二三四五六七八九十百]+)項/) {
        my $kou = $1;
        $kou = &conv2number($kou);
        $str =~ s/([〇一二三四五六七八九十百]+項)/${kou}項/;
        return($str);
    }

    if($str =~ /([一二三四五六七八九十百]+)号/) {
        my $gou = $1;
        $gou = &conv2number($gou);
        $str =~ s/([〇一二三四五六七八九十百]+号)/${gou}号/;
        return($str);
    }
    return($str);
}

     
sub convTitleNumber {
    my $str = $_[0];
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
    my $str = $_[0];
    my $type = "";
    my $year = 0;
    my $month = 0;
    my $day = 0;
    
    if($str =~ /(..)([〇一二三四五六七八九十]+)年([〇一二三四五六七八九十]+)月([〇一二三四五六七八九十]+)日/) {
         $type =  $1;
         $year = &conv2number($2);
         $year = &convYear($type,$year);
         $month = &conv2number($3);
         $day = &conv2number($4);
         if($type ne "昭和" && $type ne "平成") {
            $str =~ s/[〇一二三四五六七八九十]+年[〇一二三四五六七八九十]+月[〇一二三四五六七八九十]+日/${year}\/${month}\/${day}/;
        } else {
            $str =~ s/..[〇一二三四五六七八九十]+年[〇一二三四五六七八九十]+月[〇一二三四五六七八九十]+日/${year}\/${month}\/${day}/;
        }
        return($str);

    }

    if($str =~ /([〇一二三四五六七八九十]+)月([〇一二三四五六七八九十]+)日/) {
        $month = &conv2number($1);
        $day = &conv2number($2);
        $str =~ s/[〇一二三四五六七八九十]+月[〇一二三四五六七八九十]+日/${month}\/${day}/;
        return($str);
    }

    if($str =~ /(..)([〇一二三四五六七八九十]+)年/) {
        $type = $1;
        $year = &conv2number($2);
        $year = &convYear($type,$year);
        if($type ne "昭和" && $type ne "平成") {
            $str =~ s/[〇一二三四五六七八九十]+年/${year}年/;
        } else {
            $str =~ s/..[〇一二三四五六七八九十]+年/${year}年/;
        }
        return($str);
    }

    if($str =~ /([〇一二三四五六七八九十]+)月/) {
        $month = &conv2number($1);
        $str =~ s/[〇一二三四五六七八九十]+月/${month}月/;
        return($str);
    }

    if($str =~  /([〇一二三四五六七八九十]+)日/) {
        $day = &conv2number($1);
        $str =~ s/[〇一二三四五六七八九十]+日/${day}日/;
        return($str);
    }

    return($str);
}

sub convYear {
    my $type = $_[0];
    my $year = $_[1];

    if($type eq "昭和") {
        $year = $year + 1925;

    } elsif($type eq "平成") {
       $year = $year + 1988;
    } 

    return($year);
}
 

sub conv2number {
    my $x = $_[0];

    if($x !~ /^([〇一二三四五六七八九十百]+)$/){
        return(0);
    }

    $x =~ s/^(百)([一二三四五六七八九十]+)/1${2}/;
    $x =~ s/^([一二三四五六七八九]+)(百)$/${1}00/;
    $x =~ s/^([一二三四五六七八九]+)(百)([一二三四五六七八九]+)$/${1}0${3}/;
    $x =~ s/^([一二三四五六七八九]+)(百)([一二三四五六七八九]+)/${1}${3}/;
    $x =~ s/^([一二三四五六七八九]+)(百)(十)([一二三四五六七八九]+)/${1}1${4}/;
    $x =~ s/^([一二三四五六七八九]+)(百)([一二三四五六七八九]+)(十)/${1}${3}${4}/;
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
