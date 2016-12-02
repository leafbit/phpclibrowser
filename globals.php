<?php
global $_SESSION, $_POST;
$_POST = array();

$session_file = dirname(__FILE__) . '/default.session';
$post_file = dirname(__FILE__) . '/post.php';
$get_file = dirname(__FILE__) . '/get.php';

if (file_exists($session_file)) {
  $_SESSION = unserialize(file_get_contents($session_file));
} else {
  $_SESSION = array();
}

if (file_exists($get_file)) {
  include($get_file);
  unlink($get_file);
}

if (file_exists($post_file)) {
  include($post_file);
  unlink($post_file);
}
?>
