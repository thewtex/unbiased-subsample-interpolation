#! /usr/bin/env perl
use Cwd;

my $LogFile = "doextraction.out";
open(OLDOUT, ">&STDOUT");
open(OLDERR, ">&STDERR");
system("pwd");
open(STDOUT, ">$LogFile") or die "Could not open $LogFile: $!\n";
open(STDERR, ">&STDOUT");
select(STDERR); $| = 1;
select(STDOUT); $| = 1;

my $cmdtorun = $ARGV[0];
my $unique = $ARGV[1];
my $args = $ARGV[2];

my $jobtar = "$unique.tar.gz";

# note this brings in all job related input files
# but not the shared files across jobs.
print "Tar file to extract is <$jobtar>\n";
if(-f "$jobtar") {
	print "Tar files exists. Extract....\n";
	system("tar -zxvf $unique.tar.gz");
}

# do we have dataset shared files to extract?
if(-f "sharedfiles.tar.gz") {
    print "Shared files exist. Extracting.....\n";
    system("tar -zxvf sharedfiles.tar.gz");
    print "Done extracting\n";
}

system("df -k");
system("pwd");

print "Running here: ";
system("hostname");

system("ls -la");

system("printenv");
print "Running $cmdtorun \n";
system("chmod 755 $cmdtorun");
$res = system("./$cmdtorun $args");

print "Done Running $cmdtorun $unique with args<$args> Result was <$res>\n";
if($res != 0) {
	print "Non-zero job status so exit(1)....\n";
	system("touch FAILED");
	exit(1);
}


print "Results are:";
system("ls -l");

