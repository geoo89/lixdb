<h2>Lix level and replay database</h2>

This is a level and replay database template for <a href="https://github.com/SimonN/Lix">Lix</a>, written using Django.
Tracks and ranks statistics for levels such as number of lix saved, number of skills used, time taken.<br />

<h3>Setup</h3>
<ul>
 <li>Make sure to have <a href="https://www.djangoproject.com/download/">Django</a> installed.</li>
 <li>Place some Lix levels in <tt>media/levels/</tt> and some replays for these levels in <tt>media/replays</tt>.</li>
 <li>Set up the lix replay checker by compiling a binary or getting it from http://asdfasdf.ethz.ch and copy the <tt>bin</tt>, <tt>images</tt> and <tt>data</tt> folders over into <tt>media/</tt>.</li>
 <li>Move <tt>media/bin/lix</tt> to <tt>media/lix</tt> or create a link for <tt>media/lix</tt> to <tt>media/bin/lix</tt>.</li>
 <li>Run <tt>./populate.sh -v</tt> to generate the database from the levels and replays in their respective folders. It uses the lix replay checker to create a file <tt>replay_list.csv</tt> containing statistics about the replays. If you omit the <tt>-v</tt> option, no new <tt>replay_list.csv</tt> will be generated and the old one will be used instead (this is faster).</li>
 <li>Run <tt>python manage.py runserver</tt> and visit <tt>http://127.0.0.1:8000/lixdb/</tt> in your browser.</li>
</ul>
