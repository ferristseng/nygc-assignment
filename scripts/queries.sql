/* 1. List of all committed crimes in dataset. */
select distinct(cd.primary_type) from crime_data cd;

/* 2. For each year, what type of crime was most frequently committed
 *
 * FIXME: will need to return the top result instead of groupings.
 */
select
  date_part('year', cd.date) as crime_yr, 
  cd.primary_type,
  count(*) as freq
from crime_data cd
group by crime_yr, cd.primary_type
order by crime_yr asc, freq desc;

/* 3. Percentage primary_type that were arrests */
select
  stats.primary_type,
  stats.arrests,
  stats.total,
  100.0 * cast(stats.arrests as float) / stats.total as percent_arrests
from (
	select
	  cd.primary_type,
	  count(*) as total,
	  count(case when cd.arrest = false then 1 end) as no_arrests,
	  count(case when cd.arrest = true then 1 end) as arrests
	from crime_data cd
	group by cd.primary_type
) stats;

/* 4. YOY frequency of each crime
 *
 * Note: Could maybe use a windowing function here?
 */
select 
	date_part('year', cd.date) as crime_yr, 
	cd.primary_type,
	count(*) as freq
from crime_data cd
group by crime_yr, cd.primary_type;

/* 5. For beat, district, ward, community retrieve all unique keys of each crime incident ordered by date. */
select
	cd.unique_key,
	cd.beat,
	cd.date
from crime_data cd
where cd.beat = '811'
order by date desc;
