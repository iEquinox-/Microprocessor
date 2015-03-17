import urllib.parse,urllib.request,re,queue,sys

def communicate( said ):
	reply = str(urllib.request.urlopen(urllib.request.Request("http://www.pandorabots.com/pandora/talk?botid=afdae4b56e344e25&skin=custom_input"),(urllib.parse.urlencode([("botcust2","9a41a3f618c439e2"),("input",(' '.join(said)))])).encode('ascii'),120).read()).split("\n")[-1]
	i=0
	while reply.find("<b>ALICE:") == 0:
		reply = str(urllib.request.urlopen(urllib.request.Request("http://www.pandorabots.com/pandora/talk?botid=afdae4b56e344e25&skin=custom_input"),(urllib.parse.urlencode([("botcust2","9a41a3f618c439e2"),("input",(' '.join(said)))])).encode('ascii'),120).read()).split("\n")[i]
		i -= 1
	reply = str(reply).replace("\\n","").replace("\\","")
	start,end = """<font face="Arial" size="2">""","""<input type="hidden" name="botcust2" value="99dceb07de1c331d">"""
	ret = re.search('%s(.*)%s' % (start,end), reply).group(1)
	ret = ret.replace("""<input type="hidden" name="botcust2" value="9a41a3f618c439e2"><FORM name=f action="" method=post>""","")
	ret = ret.replace("""Go back the the <a target="_new" href="http://www.alicebot.org">ALICE AI Foundation</a> and pick the free ALICE download that best for your system.   and create your own chat robot! <p></p> Maybe you should check out the document <a target="_new" href="http://www.alicebot.org/dont.html">DON'T READ ME</a> too.""","")
	queue.Queue().put( ret )
	return ret

if __name__ == "__main__":
	print(communicate( sys.argv[1].split(" ") ))
