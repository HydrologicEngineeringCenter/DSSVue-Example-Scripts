 	
write-host "There are a total of $($args.count) arguments"
for ( $i = 0; $i -lt $args.count; $i++ ) {
    write-host "Argument  $i is $($args[$i])"
} 

Start-Process C:\Programs\CWMS-v3.2.1.256\common\exe\runhere.exe  -ArgumentList  "jython $($args[0]) $($args[1])"  -Wait -NoNewWindow


