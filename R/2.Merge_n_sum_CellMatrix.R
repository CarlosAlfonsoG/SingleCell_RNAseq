library(biomaRt);require(dplyr);require(tidyverse);
#Load all csv files giving path name tsv 
tsvs <- list.files()
All <- lapply(tsvs,function(i){
  read.table(i, header=T, sep = "\t")
})
#Replace NA with 0.0001
reduce(All, full_join, by = "gene") %>% replace(., is.na(.), 0.00001);
#Annotate data frame 
#Download MART file for the genome of interest 
mart <- useDataset("mmusculus_gene_ensembl", useMart("ensembl"))
#create an object with gene names
genes <- rownames(cell.mat)
#match gene names in data frame with ensembl genes
results <- getBM(attributes = c("mgi_symbol", "ensembl_gene_id"), filters = "ensembl_gene_id", values = genes, mart = mart)
#add extra column with gene names
merge_w_genes <- merge(merged_star_final_ensemblids, results, by ="gene", all.x = T) 
##Sum all transcripts for the same gene
sum_merge_w_genes <- merge_w_genes %>% 
  group_by(mgi_symbol) %>% 
  summarise_all(funs(sum))
Data <- as.data.frame(sum_merge_w_genes)
Data  <- Data[complete.cases(Data), ]
rownames(datas) <- datas$mgi_symbol
datas$mgi_symbol <- NULL 


##Write final 
write.csv(Data, file="Merged_Csv_file.csv")
