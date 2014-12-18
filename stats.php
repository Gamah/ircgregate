<?php
define('PAGE_CACHE_EXPIRES', 10000);
define('PAGE_CACHE_FILEPATH', './.cached_stats.html');

// Get the modification time of the cached page and
// determine if it is within the expiration time
$cached = filemtime(PAGE_CACHE_FILENAME);
$expired = ($cached !== false && $cached > (microtime(true) - PAGE_CACHE_EXPIRES));
if (!$expired) {
echo file_get_contents(PAGE_CACHE_FILENAME);
exit();
}

ob_start();
?><HTML>
<TITLE>IRCgregate - IRC Big Data Style</TITLE>
<BODY>Welcome to -Gamah's IRC aggregation project! <BR>  
The bot is:
 <?php
$check = shell_exec("ps aux | grep 'SCREEN -S bot'");
if(strstr($check,"python3")){
echo "online!";
}else{
echo "offline!";
}
header( "refresh:5");
?>
<BR>
Join irc.geekshed.net and type: "/msg statbot suggest [word]" to add a word to the list!
<BR><BR>
Current channels idling:<BR>
#jupiterbroadcasting<BR>
<BR>
<BR>
<div style="float: left; margin-right: 20px">
Suggested words, last 24 hours:
<?php
$con=mysqli_connect("127.0.0.1","changeme","changeme","ircgregate");
// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM worduse");

echo "<table border='1'>
<tr>
<th>Word</th>
<th>Count</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td>" . $row['word'] . "</td>";
  echo "<td>" . $row['count'] . "</td>";
  echo "</tr>";
}

echo "</table>";

mysqli_close($con);
?>
</div>
<div style="float: left; margin-right: 20px">
User mentions, last 24 hours:
<?php
$con=mysqli_connect("127.0.0.1","changeme","changeme","ircgregate");
// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM usermentions");

echo "<table border='1'>
<tr>
<th>User</th>
<th>Count</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td>" . $row['user'] . "</td>";
  echo "<td>" . $row['count'] . "</td>";
  echo "</tr>";
}

echo "</table>";

mysqli_close($con);
?>
</div>
<div style="float: left; margin-right: 20px">
User word count, last 24 hours:
<?php
$con=mysqli_connect("127.0.0.1","changeme","changeme","ircgregate");
// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM userwordcount");

echo "<table border='1'>
<tr>
<th>User</th>
<th>Count</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td>" . $row['user'] . "</td>";
  echo "<td>" . $row['count'] . "</td>";
  echo "</tr>";
}

echo "</table>";

mysqli_close($con);
?>
<BR>
<BR>
</div>
</BODY>
</HTML>
<?php
file_put_contents(PAGE_CACHE_FILENAME, ob_get_contents());
ob_end_flush();
