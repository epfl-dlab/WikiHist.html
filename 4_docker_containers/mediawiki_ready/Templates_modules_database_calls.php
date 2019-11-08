<?php
/*This script is used to connect the MediaWiki and the templates and modules MySQL database.

Whenever MediaWiki needs a template or module from the MySQL database this script processes
the request, finds if the needed template or module exists, gets it from the MySQL database,
formats it in the format that MediaWiki expects it, and servers it to MediaWiki. It also does
some caching to speed up the processing of the requests.

Example
-------
$db = new TMD_database("mysql";
#$conds = array("page_namespace"=>828, "page_title"=>"Some_page_title");
#$table = array("revision", "page", "user");
#echo $db->process_query($table, 'placeholder', $conds, 123);
#$table = "page";
#echo $db->process_query($table, 'placeholder', $conds, 123);
 */

class TMD_database {
	var $conn;
	var $last_row;

	function __construct($database_ip) {
		$this->last_row["id"] = -1;

		$servername = $database_ip;
		$username = "mitrevsk";
		$password = "123";
		$dbname = "mediawiki_tmd";
		# Create connection
		$this->conn = new mysqli($servername, $username, $password, $dbname);
		$this->conn->set_charset("binary");
		# Check connection
		if ($this->conn->connect_error) {
			die("Connection failed: " . $this->conn->connect_error);
		}
	}

	# These are the functions to deal with queries
	function process_query($table, $vars, $conds, $timestamp) {

		# The query is for a page, this is the first query to the DB when asking for a page.
		if ($table == "page") {
			$row = $this->find_page_by_title($table, $vars, $conds, $timestamp);
			if ($row == false) {
				return false;
			}
			return $this->page_result($row);
		}

		# The query is for a revision, page, user, this is the second query to the DB when asking for a page.
		# There are two types of queries, find by 'page_id' or find by 'page_title'
		elseif ($table[0] == "revision") {
			# Find revision by 'page_id'
			if (array_key_exists('page_id', $conds)) {
				$mysql_id = $conds['page_id'];
				$row = $this->query_MYSQL($mysql_id);

				# This is to check if the template is still valid for a given page, because of mediawiki cache!
				$current_timestamp = intval($row["new_timestamp"]);
				$valid_until_timestamp = intval($row["valid_until_timestamp"]);
				$timestamp_page = intval($timestamp);
				# If the page is older (before) than the template, query the dataset
				if ($timestamp_page < $current_timestamp) {
					$tmp_conds = array();
					$tmp_conds['page_title'] = $row["title"];
					$tmp_conds['page_namespace'] = $row["ns"];
					$page_id = $row["id"];
					$row = $this->find_page_by_title($table, $vars, $tmp_conds, $timestamp);
					return $this->revision_result($row, $page_id);
				}
				# If the template is the last one, nothing we can do
				if ($valid_until_timestamp == -1) {
					return $this->revision_result($row);
				}
				# If the page is older, than the max time the template is valid, query the dataset
				if ($timestamp_page > $valid_until_timestamp) {
					$tmp_conds = array();
					$tmp_conds['page_title'] = $row["title"];
					$tmp_conds['page_namespace'] = $row["ns"];
					$page_id = $row["id"];
					$row = $this->find_page_by_title($table, $vars, $tmp_conds, $timestamp);
					return $this->revision_result($row, $page_id);
				}
				return $this->revision_result($row);
			}
			# Find revision by 'page_title'
			else {
				$row = $this->find_page_by_title($table, $vars, $conds, $timestamp);
				if ($row == false) {
					return false;
				}
				return $this->revision_result($row);
			}
		}

		# The query is for a text, this is the third and last query to the database when asking for a page
		elseif ($table == "text") {
			$mysql_id = $conds['old_id'];
			$row = $this->query_MYSQL($mysql_id);
			return $this->text_result($row);
		}

		# The page is not a template or a module, so return false or empty page...
		else {
			return false;
		}
	}

	# Helper function for finding a page by title
	function find_page_by_title($table, $vars, $conds, $timestamp) {
		$conds['page_title'] = ucfirst($conds['page_title']);
		$conds['page_title'] = str_replace("_", " ", $conds['page_title']);

		# The page is a template (namespace: 10)
		if ($conds['page_namespace'] == 10) {
			$title = $this->conn->real_escape_string($conds['page_title']);
			$timestamp_ = $this->conn->real_escape_string($timestamp);
			$sql = "SELECT id, page_len, redirect, model, timestamp, sha1, ns, title, text, valid_until_timestamp FROM tmtable t WHERE t.ns=10 AND t.title='$title' AND t.new_timestamp<=$timestamp_ ORDER BY t.new_timestamp DESC LIMIT 1;";
			# If there is no result, returns false
			$row = $this->conn->query($sql)->fetch_assoc();
			if ($row) {
				$this->last_row = $row;
			}
			return $row;
		}

		# The page is a Lua module (namespace: 828)
		elseif ($conds['page_namespace'] == 828) {
			$title = $this->conn->real_escape_string($conds['page_title']);
			$timestamp_ = $this->conn->real_escape_string($timestamp);
			$sql = "SELECT id, page_len, redirect, model, timestamp, sha1, ns, title, text, valid_until_timestamp FROM tmtable t WHERE t.ns=828 AND t.title='$title' AND t.new_timestamp<=$timestamp_ ORDER BY t.new_timestamp DESC LIMIT 1;";
			# If there is no result, returns false
			$row = $this->conn->query($sql)->fetch_assoc();
			if ($row) {
				$this->last_row = $row;
			}
			return $row;
		}

		# The page is something else, we don't care
		else {
			return false;
		}
	}

	function page_result($row) {
		$result = array('page_id' => $row["id"], 'page_len' => $row["page_len"], 'page_is_redirect' => $row["redirect"],
			'page_latest' => $row["id"], 'page_content_model' => $row["model"], 'page_touched' => $row["timestamp"]);
		return (object) $result;
	}

	function revision_result($row, $page_id = -1) {
		if ($page_id == -1) {
			$page_id = $row["id"];
		}
		$result = array("rev_id" => $row["id"], "rev_page" => $page_id, "rev_text_id" => $row["id"], "rev_timestamp" => $row["timestamp"],
			"rev_minor_edit" => 0, "rev_deleted" => 0, "rev_len" => NULL, "rev_parent_id" => NULL, "rev_sha1" => $row["sha1"],
			"rev_comment_text" => NULL, "rev_comment_data" => NULL, "rev_comment_cid" => NULL, "rev_user" => NULL, "rev_user_text" => NULL,
			"rev_actor" => NULL, "rev_content_format" => NULL, "rev_content_model" => $row["model"], "page_namespace" => $row["ns"],
			"page_title" => $row["title"], "page_id" => $page_id, "page_latest" => $row["id"], "page_is_redirect" => $row["redirect"],
			"page_len" => $row["page_len"], "user_name" => NULL);
		return (object) $result;
	}

	function text_result($row) {
		$result = array('old_text' => $row["text"], 'old_flags' => "utf-8");
		return (object) $result;
	}

	function query_MYSQL($id) {
		if ($id == $this->last_row["id"]) {
			return $this->last_row;
		}
		$sql = "SELECT id, page_len, redirect, model, timestamp, sha1, ns, title, text, valid_until_timestamp FROM tmtable WHERE id = " . $id;
		$row = $this->conn->query($sql)->fetch_assoc();
		$this->last_row = $row;
		return $row;
	}
}

?>
