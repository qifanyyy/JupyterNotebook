import sys
import json
import time


def getHistogramSQL(domainResilienceDict, saveFilePath):
  result = ""
  result += "TRUNCATE TABLE as_resiliance;\n\n"
  #Add a printing loop
  for domainAS, resiliance in domainResilienceDict.items():
    result += "INSERT INTO as_resiliance VALUES ('" + str(domainAS) + "', " + str(resiliance) + ");\n"
  
  result += """
SELECT 'Generating origin table.' AS '';
CREATE TEMPORARY TABLE IF NOT EXISTS originASTable AS (SELECT SUBSTRING_INDEX(SUBSTRING_INDEX(resolvedAsPath, ' ', -2), ' ', 1) AS originAS From routeAges where resolvedAsPath is not null);


SELECT 'Dropping weightedResiliance.' AS '';
DROP TABLE weightedResiliance;

SELECT 'Creating weightedResiliance.' AS '';
CREATE TEMPORARY TABLE IF NOT EXISTS weightedResiliance AS (select ASN, resiliance from as_resiliance RIGHT JOIN originASTable ON ASN = originAS);

SELECT 'Dropping groupedResilience.' AS '';
DROP TABLE groupedResilience;

SELECT 'Creating groupedResilience.' AS '';
CREATE TEMPORARY TABLE IF NOT EXISTS groupedResilience AS (select ASN, avg(resiliance) as resiliance, count(ASN) as numberOfDomains from weightedResiliance group by ASN);
"""
  
  result += """
SELECT 'Running histogram code.' AS '';
# Full Histogram code:
set @csum := 0;
SELECT count(*) FROM weightedResiliance INTO @total;
select resiliance,
       (@csum := @csum + numberOfDomains) / @total as cumulative_sum
       from groupedResilience
       order by resiliance
INTO OUTFILE '{0}'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
""".format(saveFilePath)
  return result

