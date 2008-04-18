#!/usr/bin/python

'''ISO 15919 transliteration for devanagari text.

Simple usage:

    import iso15919
    romanised_unicode = iso15919.transliterate(indic_unicode)


Copyright (c) 2008 by Mublin <mublin@dealloc.org>
This module is free software, and you may redistribute it and/or modify
it under the same terms as Python itself, so long as this copyright message
and disclaimer are retained in their original form.

IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.'''

__author__ = "Mublin <mublin@dealloc.org>"
__date__ = "16 April 2008"
__version__ = "0.1.6"

class TransliterationError(Exception):
    pass

DEVANAGARI_START   = u'\u0901'
CANDRABINDU        = u'\u0901'
ANUSVARA           = u'\u0902'
VISARGA            = u'\u0903'
VOWEL_START        = u'\u0904'
VOWEL_END          = u'\u0914'
CONSONANT_START    = u'\u0915'
CONSONANT_END      = u'\u0939'
NUKTA              = u'\u093c'
AVAGRAHA           = u'\u093d'
MATRA_START        = u'\u093e'
MATRA_END          = u'\u094c'
VIRAMA             = u'\u094d'
OM                 = u'\u0950'
UDATTA             = u'\u0951'
ANUDATTA           = u'\u0952'
GRAVE              = u'\u0953'
ACUTE              = u'\u0954'
CONSONANT2_START   = u'\u0958'
CONSONANT2_END     = u'\u095f'
VOWEL2_START       = u'\u0960'
VOWEL2_END         = u'\u0961'
MATRA2_START       = u'\u0962'
MATRA2_END         = u'\u0963'
PUNCTUATION_START  = u'\u0964'
DANDA              = u'\u0964'
DOUBLEDANDA        = u'\u0965'
PUNCTUATION_END    = u'\u0965'
DIGIT_START        = u'\u0966'
DIGIT_END          = u'\u096f'
PUNCTUATION2_START = u'\u0970'
PUNCTUATION2_END   = u'\u0971'
VOWEL3             = u'\u0972'
CONSONANT3_START   = u'\u097b'
CONSONANT3_END     = u'\u097c'
GLOTTALSTOP        = u'\u097d'
CONSONANT4_START   = u'\u097e'
CONSONANT4_END     = u'\u097f'
DEVANAGARI_END     = u'\u097f'

table = u'''\
\u0901	m\u0310
\u0902	\u1e41
\u0903	\u1e25
\u0904	
\u0905	a
\u0906	\u0101
\u0907	i
\u0908	\u012b
\u0909	u
\u090a	\u016b
\u090b	\u1e5b
\u090c	\u1e37
\u090d	
\u090e	
\u090f	e
\u0910	ai
\u0911	\u00f4
\u0912	
\u0913	o
\u0914	au
\u0915	ka
\u0916	kha
\u0917	ga
\u0918	gha
\u0919	\u1e45a
\u091a	ca
\u091b	cha
\u091c	ja
\u091d	jha
\u091e	\xf1a
\u091f	\u1e6da
\u0920	\u1e6dha
\u0921	\u1e0da
\u0922	\u1e0dha
\u0923	\u1e47a
\u0924	ta
\u0925	tha
\u0926	da
\u0927	dha
\u0928	na
\u0929	n\u0331a
\u092a	pa
\u092b	pha
\u092c	ba
\u092d	bha
\u092e	ma
\u092f	ya
\u0930	ra
\u0931	r\u0331a
\u0932	la
\u0933	
\u0934	l\u0331a
\u0935	va
\u0936	\u015ba
\u0937	\u1e63a
\u0938	sa
\u0939	ha
\u093c	
\u093d	'
\u093e	\u0101
\u093f	i
\u0940	\u012b
\u0941	u
\u0942	\u016b
\u0943	\u1e5b
\u0944	\u1e5d
\u0945	\u00ea
\u0946	
\u0947	e
\u0948	ai
\u0949	\u00f4
\u094a	
\u094b	o
\u094c	au
\u094d	
\u0950	o\u1e43
\u0951	
\u0952	
\u0953	
\u0954	
\u0958	qa
\u0959	k\u0331h\u0331a
\u095a	\u0121
\u095b	za
\u095c	\u1e5ba
\u095d	\u1e5bha
\u095e	fa
\u095f	\u1e8fa
\u0960	\u1e5d
\u0961	\u1e39
\u0962	\u1e37
\u0963	\u1e39
\u0964	.
\u0965	..
\u0966	
\u0967	
\u0968	
\u0969	
\u096a	
\u096b	
\u096c	
\u096d	
\u096e	
\u096f	
\u0970	\u2026
\u0971	
\u0972	
\u097b	
\u097c	
\u097d	
\u097e	
\u097f	'''

# These are special transliterations for consonant triples which have
# a virama in the centre, as well as for some consonant-nukta pairs
# which are not equivalent to a single Unicode character.
clusters = u'''\
\u0939\u093c	h\u0324a
\u0938\u093c	s\u0324a
\u0924\u093c	t\u0324a
\u0915\u094d\u0937	k\u1e63a
\u091c\u094d\u091e	j\xf1a
\u0924\u094d\u0930	tra
\u0936\u094d\u0930	\u015bra'''

# These are combinations of consonant and nukta which are equivalent
# to a single Unicode character.
nukta_consonants = u'''\
\u0929	\u0928\u093c
\u0931	\u0930\u093c
\u0934	\u0933\u093c
\u0958	\u0915\u093c
\u0959	\u0916\u093c
\u095a	\u0917\u093c
\u095b	\u091c\u093c
\u095c	\u0921\u093c
\u095d	\u0922\u093c
\u095e	\u092b\u093c
\u095f	\u092f\u093c'''

table = [row.split('\t') for row in table.split('\n')]
clusters = dict(row.split('\t') for row in clusters.split('\n'))
clusterables = dict.fromkeys(cluster[0] for cluster in clusters)
nukta_consonants = dict(row.split('\t') for row in nukta_consonants.split('\n'))

iso15919 = {}
for char, trans in table:
    if trans:
        iso15919[char] = trans
        
def transliterate(source):
    '''Transliterate Devanagari to the Latin alphabet (ISO 15919).

    transliterate(unicode) -> unicode

    If a unicode character from the Devanagari range cannot be
    transliterated, a TransliterationError is raised. If another
    unicode character cannot be transliterated, it is copied unchanged
    to the result string.

    - simplified nasalization option: anusvara is transliterated U+1E41
      and candrabindu mU+0310.

    - non-uniform vowel option: The vowels e and o will not be marked
      long, as usual for scripts not having short e and o.

    TODO:

    - implement strict options
    - provide transliterations for rare characters
    - check danda and double danda transliteration

    SOURCES: 

    - http://www.unicode.org/charts/PDF/U0900.pdf
    - http://transliteration.eki.ee/pdf/Hindi-Marathi-Nepali.pdf
    - http://homepage.ntlworld.com/stone-catend/triunico.htm'''

    # normalisation: replace consonant + nukta by equivalent
    # consonants
    orig = source
    for char, combination in nukta_consonants.iteritems():
        source = source.replace(combination, char)

    # transliterate character by character
    result, i = [], 0
    while i < len(source):
        char = source[i]

        # consonant + virama or matra?
        if i and (char == VIRAMA or
                  MATRA_START <= char <= MATRA_END or
                  MATRA2_START <= char <= MATRA2_END):
            prev = source[i-1]
            if prev != NUKTA or i > 1:
                if prev == NUKTA:
                    prev = source[i-2]
                if (CONSONANT_START <= prev <= CONSONANT_END or
                    CONSONANT2_START <= prev <= CONSONANT2_END):
                    consonant = result[-1]
                    if consonant.endswith('a'):
                        if char == VIRAMA:
                            result[-1] = consonant[:-1]
                        else:
                            result[-1] = consonant[:-1] + iso15919[char]
                        i += 1
                        continue

        # special transliteration for consonant cluster?
        if char in clusterables:
            try:
                next = source[i+1]
            except IndexError:
                pass
            else:
                try:
                    if next == VIRAMA:
                        result.append(clusters[source[i:i+3]])
                        i += 3
                        continue
                    elif next == NUKTA:
                        result.append(clusters[source[i:i+2]])
                        i += 2
                        continue
                except KeyError:
                    pass

        # vowel + nukta?
        if i and char == NUKTA:
            prev = source[i-1]
            if VOWEL_START <= prev <= VOWEL_END \
                    or VOWEL2_START <= prev <= VOWEL2_END \
                    or VOWEL3 == prev \
                    or MATRA_START <= prev <= MATRA_END \
                    or MATRA2_START <= prev <= MATRA2_END:
                result.append(u'\u2018')
                i += 1
                continue

        # default.
        try:
            result.append(iso15919[char])
        except KeyError:
            if DEVANAGARI_START <= char <= DEVANAGARI_END:
                start, end = i - 3, i + 3
                if start < 0:
                    start, end = 0, end - start
                raise TransliterationError, \
                    'no transliteration for Devanagari %r (%r)' % (char, source[start:end])
            result.append(char)

        i += 1

    return ''.join(result)

if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        sys.stdout.write(
            transliterate(line.decode('utf-8')).encode('utf-8'))
