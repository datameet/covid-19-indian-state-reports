* prelim 
clear 
global path "C:/Users/aadit/Documents/GitHub/covid-19-indian-state-reports"

* get files 
* ssc install filelist 
filelist, dir("$path") p("*.pdf")

* mop up 
split filename, p("-")
rename filename1 iso_state
rename filename2 yr
rename filename3 mm 

* define date 
cap drop dd 
gen dd = regexs(0) if regexm(filename4, "^[0-9][0-9]") == 1 
egen date = concat(yr mm dd), p("-")
destring mm dd yr, replace
gen dt = mdy(mm, dd, yr)
format dt %td 

* state 
replace iso_state = upper(iso_state)
encode iso_state, gen(state)

* some states have multiple reports within a day 
duplicates drop state dt, force

* set as panel 
xtset state dt 

* make balanced panel
fillin state dt 

* is the data available?
gen yes_data = dd != . 

* graph 
xtline yes, xtitle("Date") ytitle("Data Availability") ///
ylabel(#2) xlabel(, angle(45)) note("") xla(, tlc(black)) yla(, tlc(black))

* export 
graph export "$path/summaries/data_summary_2020_04_03.png", replace 



