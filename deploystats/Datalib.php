<?php

class Datalib {
  private $file;
  private $xml;

  public function __construct($file) {
    $this->file = $file;
    $this->xml = simplexml_load_file($file);
  }

  public function __toString() {
    return $this->xml->asXML();
  }

  private function save() {
    return $this->xml->asXML($this->file);
  }

  public function exists($ip, $url) {
    if ($this->xml->xpath("/sites/site[ip='$ip'][url='$url']/siteName")) {
      return true;
    } else {
      return false;
    }
  }

  public function insert($ip, $url, $siteName, $country, $public, $contactName,
      $contactEmail, $release, $notifications) {
    $site = $this->xml->addChild('site');
    $site->addChild('ip', $ip);
    $site->addChild('url', $url);
    $site->addChild('siteName', $siteName);
    $site->addChild('country', $country);
    $site->addChild('public', $public);
    $site->addChild('contactName', $contactName);
    $site->addChild('contactEmail', $contactEmail);
    $site->addChild('release', $release);
    $site->addChild('notifications', $notifications);
    $site->addChild('status', 'accepted');
    return $this->save();
  }

  public function showAccepted() {
    return $this->xml->xpath("/sites/site[status='accepted']");
  }

  public function showNew() {
    return $this->xml->xpath("/sites/site[status='new']");
  }

  public function showDenied() {
    return $this->xml->xpath("/sites/site[status='denied']");
  }

  public function updateStatus($ip, $url, $newStatus) {
    $sel = $this->xml->xpath("/sites/site[ip='$ip'][url='$url']");
    print_r($sel);
    print "second";
    $sel[0]->status = $newStatus;
    print_r($sel);
    return $this->save();
  }

  public function delete($ip, $url) {
    list($theNodeToBeDeleted) = $this->xml->xpath("/sites/site[ip='$ip'][url='$url']");
    $oNode = dom_import_simplexml($theNodeToBeDeleted);
    $oNode->parentNode->removeChild($oNode);
    return $this->save();
  }
}

?>
