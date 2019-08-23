select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 1 
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE 'q1.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 2 
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE 'q2.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';


select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 3 
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE 'q3.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 4
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE 'q4.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 5
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE 'q5.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 6
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE 'q6.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select 'UserId', 'Response'
Union ALL
select user_id, response 
from responses 
where question_id = 7
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf')
INTO OUTFILE '/var/lib/mysql-files/q7.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"';

select 'SentenceID', 'Technique', 'User_ID', 'Response'
UNION ALL
select sentence_id, technique, user_id, response
from responses, sentences
where responses.sentence_id = sentences.id
and sentence_id > 0
and question_id = 8
and user_id in 
('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf');
211 


select technique, count(*) 
from sentences, responses 
where sentences.id = responses.sentence_id 
and sentence_id > 0
and question_id=8
and (technique = 3 or technique = 4 or technique = 5 or technique = 10)
and user_id in ('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'1e291d9f8c99470ffa480486a34873f5',
'5670aa00131590317912dac744b3177e',
'46a48d98a47aeb653879015c3361fa64',
'5c1e42105e8b0f72d95a7580f24fb393')
group by technique ;


#wordpattern
select technique, sentence_id, count(*) 
from sentences, responses 
where sentences.id = responses.sentence_id 
and sentence_id > 0
and question_id=8
and (technique = 3 or technique = 4 or technique = 5 or technique = 9 or technique = 10)
and user_id in ('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'1e291d9f8c99470ffa480486a34873f5',
'5670aa00131590317912dac744b3177e',
'46a48d98a47aeb653879015c3361fa64',
'5c1e42105e8b0f72d95a7580f24fb393')
group by technique, sentence_id ;



#ifsentence
select technique, sentence_id, count(*) 
from sentences, responses 
where sentences.id = responses.sentence_id 
and sentence_id > 0
and question_id=8
and (technique = 1 or technique = 4 or technique = 7 or technique = 10)
and user_id in ('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'1e291d9f8c99470ffa480486a34873f5',
'5670aa00131590317912dac744b3177e',
'46a48d98a47aeb653879015c3361fa64',
'5c1e42105e8b0f72d95a7580f24fb393')
group by technique, sentence_id ;


#all techniques
select 'SentenceID', 'Technique', 'Count'
UNION ALL
select  sentence_id, technique, count(*) 
from sentences, responses 
where sentences.id = responses.sentence_id 
and sentence_id > 0
and question_id=8
and user_id in ('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'1e291d9f8c99470ffa480486a34873f5',
'5670aa00131590317912dac744b3177e',
'46a48d98a47aeb653879015c3361fa64',
'5c1e42105e8b0f72d95a7580f24fb393')
group by technique, sentence_id ;


select 'ThreadID', 'Count'
UNION ALL
select  thread_id, count(DISTINCT user_id) 
from sentences, responses 
where sentences.id = responses.sentence_id 
and sentence_id > 0
and question_id=8
and user_id in ('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'1e291d9f8c99470ffa480486a34873f5',
'5670aa00131590317912dac744b3177e',
'46a48d98a47aeb653879015c3361fa64',
'5c1e42105e8b0f72d95a7580f24fb393')
group by thread_id;

Sarah test: a5bcfdd4053d957fe60c0281b8efccd9
e1c146b8b9a2baf57f8565fe5bcc3850
5e03e9fd95f2df84b0ddc9aed5bce4ef
cd735bcd77a6808c7b078e6814c3c7a9
fb48e4780f492ef3032ff29b3f9b992a
select 'ThreadID', 'Count'
UNION ALL
select  thread_id, count(DISTINCT user_id) as numresp 
from sentences, responses 
where sentences.id = responses.sentence_id 
and sentence_id > 0
and user_id in ('1abff8f3c01fdafd3bcd19f87c394ce4',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'e65bb7c765458b48e9ecc690c047e57e',
'ff6c7319934da003d2cc3cf520715006',
'5ae06be6dd4e8581d5c90c40188c4897',
'86a32f171475d4ad42af11c4cbb1eaf1',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'008b58b84d46a50e0332032e0d3d9e3a',
'd6cef22e92c1343285684a3e993e6bd3',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'c0987233440ef3ca8ad15efbe319b9fe',
'2a8581d33179ed475cf9cfcada387e57',
'1bd1c455f2839dc7cbc6251537f3da8c',
'b5c68f66246b451c0f65518977e7a241',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'5c1e42105e8b0f72d95a7580f24fb393',
'1e291d9f8c99470ffa480486a34873f5',
'46a48d98a47aeb653879015c3361fa64',
)
group by thread_id
order by numresp;


select  user_id
from responses 
where sentence_id = -1
and question_id=10
and (response = 'Disagree' or response = 'Strongly disagree')
and user_id in ('c0987233440ef3ca8ad15efbe319b9fe',
'ff6c7319934da003d2cc3cf520715006',
'86a32f171475d4ad42af11c4cbb1eaf1',
'1bd1c455f2839dc7cbc6251537f3da8c',
'008b58b84d46a50e0332032e0d3d9e3a',
'a3f1676dc2e47d8d53c2a7c129a67b30',
'2a8581d33179ed475cf9cfcada387e57',
'7f9418fde2cfedcdde148dbdbb94d5fe',
'd6cef22e92c1343285684a3e993e6bd3',
'b5c68f66246b451c0f65518977e7a241',
'd1a66d7119f95c8f2c9361ec9f55a951',
'e65bb7c765458b48e9ecc690c047e57e',
'2a762ca4dbe190c3bdbc407a139d1b9e',
'1abff8f3c01fdafd3bcd19f87c394ce4',
'3e51e4b28d98fafdb6af2a476e01ca7a',
'7e3cb0478c410a6d14f3f7499ab52a98',
'5ae06be6dd4e8581d5c90c40188c4897',
'e00a907093d3662aa176f39e14952433',
'5857532ecc165a002982034e30107bdf',
'1e291d9f8c99470ffa480486a34873f5',
'5670aa00131590317912dac744b3177e',
'46a48d98a47aeb653879015c3361fa64',
'5c1e42105e8b0f72d95a7580f24fb393');