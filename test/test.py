import re

math_c = """"<math xmlns="http://www.w3.org/1998/Math/MathML" xmlns:cellml="http://www.cellml.org/cellml/2.0#">
      <apply>
                <eq/>
                <apply>
                    <diff/>
                    <bvar>
                        <ci>t</ci>
                    </bvar>
                    <ci>q_3</ci>
                </apply>
                <apply>
                    <plus/>
                    <ci>v_3</ci>
                    <ci>v_1</ci>
                </apply>
            </apply>
    </math>"""
math_c_reg=math_c.replace('\n','')
regex = r'(<math[^>]*>)(.*?)(</math>)'
math_match = re.findall(regex, math_c_reg)
#for tuple in math_match:
 #   print(''.join(tuple))
#print(math_match)
# find the left side of the equation in the math_c using regex, such as v_ss
regex = r'<apply>\s*<eq/>\s*<ci>(.*?)</ci>\s*<apply>'
regex = r'<apply>\s*<eq/>\s*<apply>\s*<diff/>\s*<bvar>\s*<ci>(.*?)</ci>\s*</bvar>\s*<ci>(.*?)</ci>\s*</apply>'

math_match = re.findall(regex, math_c_reg)
for tuple in math_match:
    print(tuple)
print(math_match)
