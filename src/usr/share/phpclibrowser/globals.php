<?php
global $_SESSION, $_POST;
$_POST = array();

$session_file = dirname(__FILE__) . '/' . SESSION_KEY;
$post_file = dirname(__FILE__) . '/post';
$get_file = dirname(__FILE__) . '/get';
$query_file = dirname(__FILE__) . '/query';

if (file_exists($session_file)) {
  $_SESSION = unserialize(file_get_contents($session_file));
} else {
  $_SESSION = array();
}

/**
 * Parses the raw field key into an array field key code.
 */
function __globals__fieldK($rawk) {
    $k = preg_replace(array("/\[/", "/\]/", "/^\w+/"),
      array("['", "']", "['\$0']"), $rawk);
    return $k;
}
/**
 * Loads field values from a file recorded by phpCliBroser program.
 */
function getFieldsFromFile($fname){
  $flds = array();
  if (!file_exists($fname)) return array();
  $lines = file($fname);
  $isTextArea = FALSE;
  foreach($lines as $ll) {
    $l = trim($ll);
    
    if (preg_match("/^<\!CDATA\+\+\+ textarea start\:(.*?)$/", $l, $mt)){
      $isTextArea = TRUE;
      $k = __globals__fieldK($mt[1]);
      eval("\$flds$k='';");
      eval("\$textAreaVal = &\$flds$k;");
      continue;
    }

    if ($l == '>>textarea end]]+++>'){
      $isTextArea = FALSE;
      eval("\$flds$k = trim(\$flds$k);");
      continue;
    }

    if ($isTextArea) {
      //$textAreaVal += $ll;
      $code = "\$flds$k .= \$ll;";
      eval($code);
      continue;
    }

    if (preg_match("/^FLD\:(.*?)\=(.*?)$/", $l, $mt)) {
      $k = __globals__fieldK($mt[1]);
      if (!$k) continue;
      $code = "\$flds$k=\$mt[2];";
      eval($code);
    }

  }
  unlink($fname);
  return $flds;
}

$_GET = array();
if (file_exists($query_file)) {
  $query = trim(file_get_contents($query_file));
  foreach (explode('&', $query) as $chunk) {
    $param = explode("=", $chunk);
    $k = __globals__fieldK($param[0]);
    if (!$k) continue;
    eval("\$_GET$k = \$param[1];");
  }
  unlink($query_file);
}
$_GET += getFieldsFromFile($get_file);
$_POST = getFieldsFromFile($post_file);
?>
