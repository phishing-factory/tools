#!/bin/bash
#author: mp
#comment: generate a decent sized wordlist off of only a single word like CompanyXYZ

wordlist=$1
outlist=$2
words=""
count=0
spinner=( '|' '/' '-' '\' )

#substitutions for 1337 speak
a (){ echo $1 | sed 's/a/4/g' ; }
b (){ echo $1 | sed 's/b/8/g' ; }
e (){ echo $1 | sed 's/e/3/g' ; }
g1 (){ echo $1 | sed 's/g/9/g' ; }
g2 (){ echo $1 | sed 's/g/6/g' ; }
i (){ echo $1 | sed 's/i/1/g' ; }
l (){ echo $1 | sed 's/l/1/g' ; }
o (){ echo $1 | sed 's/o/0/g' ; }
s (){ echo $1 | sed 's/s/5/g' ; }
t (){ echo $1 | sed 's/t/7/g' ; }
e (){ echo $1 | sed 's/e/3/g' ; }

#spin while adding words
append (){
  echo -e $1 >> $outlist ;
  echo -en ${spinner[$( expr $count % ${#spinner[@]} )]}
  echo -en "\x08"
  count+=1
  if [[ $count -gt 3 ]] ; then
    count=0
  fi
}

echo -en "[+] Working "
cat $wordlist | while read line ; do 
  for number in 123 234 345 456 567 678 789 1 2 3 4 5 6 7 8 9 2015 2016 2014 ; do 
    for i in {$line,$number}:{$line,$number} ; do 
      f=$( echo -e $i | cut -f1 -d: ) ; 
      s=$( echo -e $i | cut -f2 -d: ) ;
      if [[ $f != $s ]] ; then
        append $( echo -e $i | tr -d ":" ) ;
        for sub1 in a b e g1 g2 i l o s t e ; do
          first=$( echo -e $( $sub1 $i ) | tr -d ":" ; ) ;
          append $first ;
          for sub2 in a b e g1 g2 i l o s t e ; do
            second=$( $sub2 $first ) ;
            append $second ;
          done ;
        done ;
      fi ;
      done ;
    done ; #exclamation marks break stuff, so to be consitant use hex for all special chars
    for char in "\x21" "\x40" "\x23" "\x24" "\x25" "\x5E" "\x26" "\x2A" ; do 
      for j in {$line,$number,$char}:{$line,$number,$char}:{$line,$number,$char} ; do
        f=$( echo -e $j | cut -f1 -d: ) ;
        s=$( echo -e $j | cut -f2 -d: ) ;
        t=$( echo -e $j | cut -f3 -d: ) ;
        if [[ $f != $s ]] ; then
          if [[ $f != $t ]] ; then
            if [[ $s != $t ]] ; then
              append $( echo -e $j | tr -d ":" );
              for sub1 in a b e g1 g2 i l o s t e ; do
                first=$( echo -e $( $sub2 $j ) | tr -d ":" ; ) ;
                append $first
                for sub2 in a b e g1 g2 i l o s t e ; do
                  second=$( $sub2 $first ) ;
                  append $second ;
                done ;
              done ;
            fi ;
          fi ;
        fi ;
      done ;
    done ;
  done ;
echo -en "\n[+] Removing duplicates..."
cat $outlist | sort -u > _ && mv _ $outlist 
echo -en "\n[+] Generated $(wc -l $outlist | awk '{print $1}' ) passwords\n"
