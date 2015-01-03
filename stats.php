<HTML>
<?php
$time = microtime();
$time = explode(' ', $time);
$time = $time[1] + $time[0];
$start = $time;
?>
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
header( "refresh:30");
?>
<BR>
Join irc.geekshed.net and type: "/msg statbot suggest [word/smiley] {text}" to add a word to the list!
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

$result = mysqli_query($con,"SELECT * FROM wordUse2");

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

$result = mysqli_query($con,"SELECT * FROM usermentions2");

echo "<table border='1'>
<tr>
<th>User</th>
<th>Times Mentioned</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td>" . $row['user'] . "</td>";
  echo "<td>" . $row['mentions'] . "</td>";
  echo "</tr>";
}

echo "</table>";

mysqli_close($con);
?>
</div>
<div style="float: left; margin-right: 20px">
User message count, last 24 hours:
<?php
$con=mysqli_connect("127.0.0.1","changeme","changeme","ircgregate");
// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM userWordCount2");

echo "<table border='1'>
<tr>
<th>User</th>
<th>Messages</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td><a href=\"http://gamah.net/ircgregate/usermessages.php?user=" . $row['user'] . "\">" . $row['user'] . "</a></td>";
  echo "<td>" . $row['messages'] . "</td>";
  echo "</tr>";
}

echo "</table>";
mysqli_close($con);
?>
<BR>
<BR>
</div>
<div style="float: left; margin-right: 20px">
Hyperlinks posted, last 24 hours:
<?php
$con=mysqli_connect("127.0.0.1","changeme","changeme","ircgregate");
// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM hyperlinks");

echo "<table border='1'>
<tr>
<th>Url</th>
<th>Count</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td><a href=\"" . $row['url'] . "\">" . substr($row['url'], 0, 40) . "</a></td>";
  echo "<td>" . $row['Count'] . "</td>";
  echo "</tr>";
}

echo "</table>";
mysqli_close($con);
?>
<BR>
<BR>
</div>
<div style="float: left; margin-right: 20px">
Smiley count, last 24 hours:
<?php
$con=mysqli_connect("127.0.0.1","changeme","changeme","ircgregate");
// Check connection
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}

$result = mysqli_query($con,"SELECT * FROM smileyuse");

echo "<table border='1'>
<tr>
<th>Smiley</th>
<th>Count</th>
</tr>";

while($row = mysqli_fetch_array($result)) {
  echo "<tr>";
  echo "<td>" . $row['smiley'] . "</a></td>";
  echo "<td>" . $row['count'] . "</td>";
  echo "</tr>";
}

echo "</table>";
mysqli_close($con);
?>
<BR>
<BR>
<?php
$time = microtime();
$time = explode(' ', $time);
$time = $time[1] + $time[0];
$finish = $time;
$total_time = round(($finish - $start), 4);
echo 'Page generated in '.$total_time.' seconds.';
?>
<BR>
<BR>
</div>
</BODY>
</HTML>
