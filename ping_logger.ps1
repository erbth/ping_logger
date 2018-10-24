# This file is dedicated to the public domain.

$remote_address = "192.168.x.x"

# Time that the script waits at least between ping attempts
$time_delay = 60

# File to write to
$logfile = "C:\000\x.txt"

function print_ok () {
    write-host -nonewline "[  "
    write-host -nonewline -foregroundcolor green "ok"
    write-host "  ]"
}

function print_failed () {
    write-host -nonewline "["
    write-host -nonewline -foregroundcolor red "failed"
    write-host "]"
}

while ($true) {
    write-host -nonewline "Attempting to ping $remote_address ... "

    # Get current date and time
    $datetime = Get-Date

    # See https://janegilring.wordpress.com/2011/10/23/test-connection-error-handling-gotcha-in-powershell-2-0/
    try {
        $ping_status = test-connection -count 1 -computername $remote_address -erroraction stop
        print_ok

        # Write to file
        "$($datetime.year)-$($datetime.month)-$($datetime.day) $($datetime.hour):$($datetime.minute):$($datetime.second) $remote_address ok $($ping_status.responsetime)" >> $logfile
    } catch {
        print_failed

        # Write to file
        "$($datetime.year)-$($datetime.month)-$($datetime.day) $($datetime.hour):$($datetime.minute):$($datetime.second) $remote_address failed" >> $logfile
    }

    sleep $time_delay
}
