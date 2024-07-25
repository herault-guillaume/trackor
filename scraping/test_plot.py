import pandas as pd
import altair as alt
import io

# 1. Create DataFrame (using io.StringIO)
data = """
Lingot or 1 kg LBMA	-1.35	1.6	1.50051018188301	-1.31340706714822
Lingot or 500 g LBMA	-1.35	2.0	1.88677135060172	-1.31340706714822
20 lire or umberto I	-1.0	2.2	1.99550145541148	-1.04220453473066
20 lire or vittorio emanuele II	-1.0	2.2	1.99550145541148	-1.04220453473066
Lingot or 250 g LBMA	-1.35	2.2	2.07897307101995	-1.31337777752081
Lingot or 100 g LBMA	-1.35	2.3	2.17451909673821	-1.3133777775208
50 pesos or	-1.25	2.6	2.4605839578376	-1.21096773448241
50 écus or charles quint	-1.0	2.7	2.54309593542396	-0.968360365701166
souverain or georges V	-1.15	2.8	2.63754004815256	-1.08020850166525
souverain or victoria jubilee	-1.15	2.8	2.63754004815256	-1.08020850166525
20 francs or union latine léopold II	-1.0	2.9	2.66052612715934	-1.04220453473066
20 francs or tunisie	-1.0	2.9	2.74436718992663	-0.955174212133994
10 florins or wilhelmina	-1.25	2.9	2.74591428113771	-1.14354096173092
100 couronnes or françois joseph I	-1.0	2.9	2.75123671699587	-0.948768276494121
10 florins or willem III	-1.25	2.9	2.87438731379143	-1.00992994328742
Lingot or 50 g LBMA	-0.95	3.2	3.02772373540855	-0.904394996890328
1 oz krugerrand	-1.25	3.2	3.02852357639782	-1.2206105335494
souverain or elizabeth II	-1.15	3.4	3.20273667942024	-1.08020850166525
20 francs or coq marianne	-0.75	3.5	3.2247191011236	-0.786902078327417
20 francs or napoléon III	-0.75	3.5	3.2247191011236	-0.786902078327417
20 francs or génie debout	-0.75	3.5	3.2247191011236	-0.786902078327417
20 francs or cérès	-0.75	3.5	3.2247191011236	-0.786902078327417
Lingot or 1 once LBMA	-0.95	3.6	3.40358362983022	-0.914169648602241
20 francs or vreneli croix suisse	-0.25	3.8	3.48774722281436	-0.299895001478846
1 oz philharmonique	-1.25	3.7	3.49582913328734	-1.2206105335494
1 oz maple leaf	-1.25	3.9	3.68191770546054	-1.2206105335494
Lingot or 20 g LBMA	-0.75	4.1	3.86630594842641	-0.701139351446099
10 pesos or	-1.25	4.3	4.05053138159214	-1.21057799684239
1 oz nugget / kangourou	-1.0	4.5	4.23548204531991	-0.965114212140034
20 mark or wilhelm II	-1.0	4.9	4.49198989956522	-1.06780502524694
1 oz american eagle	1.0	4.9	4.60003059360329	1.03424036209119
20 couronnes or françois joseph I	-1.0	4.9	4.6312697775995	-0.921540023612747
1/2 oz nugget / kangourou	0.85	5.5	5.12935286192359	0.884371175267104
Lingot or 10 g LBMA	-0.25	5.5	5.14165224913494	-0.195848581884722
10 dollars or liberté	0.0	5.9	5.49757389724634	0.00766248542253554
20 dollars or liberté	0.0	5.9	5.49817701807767	0.0441549769681415
demi souverain or georges V	1.0	5.9	5.50060704168352	1.04318944566602
4 ducats or	0.0	6.9	6.38409339515793	0.054181197288771
Lingot or 5 g LBMA	0.0	7.2	6.64573800148983	0.0556125941136189
8 florins 20 francs or franz joseph I	0.0	7.5	6.8257936144909	-0.0311365983183212
1/2 oz maple leaf	0.85	7.5	6.89442956340743	0.884371175267104
1/2 oz krugerrand	0.85	5.6	6.94388210570192	2.68797990452377
1/2 oz american eagle	2.0	8.2	7.49729977116705	2.00180456535615
5 pesos or	-1.25	8.8	8.01936250524255	-1.21057799684239
1 ducat or	1.0	8.9	8.10429751436944	1.04405499692182
20 francs or helvetia suisse	1.0	9.5	8.52869459787148	0.957486611489791
50 francs or napoléon III tête nue	1.0	9.5	8.56904174257994	1.00300432024287
1/4 oz nugget / kangourou	2.5	9.4	8.56975890897515	2.54241296067808
5 dollars or liberté	4.0	10.0	8.98582288955162	3.86005159996355
1/4 oz krugerrand	2.5	8.5	9.49487803229948	4.32211683922536
1/4 oz maple leaf	2.5	10.9	9.80734472614285	2.54241296067808
1/4 oz american eagle	3.25	11.5	10.2921637926783	3.25000639068381
10 couronnes or françois joseph I	0.0	11.9	10.5962981532548	0.0881943989901327
1/10 oz american eagle	4.0	13.5	11.8391566021731	3.89877876730447
20 pesos or	-1.25	13.7	11.9830772060668	-1.21057799684239
Lingot or 1 g	3.0	13.9	12.1322148491298	2.96414232313444
1/10 oz nugget / kangourou	3.0	13.9	12.1372730566402	2.96617254273504
4 florins 10 francs 1892 refrappe	3.0	14.0	12.2144582470669	2.96553205709649
10 francs or napoléon III	4.0	14.4	12.4446808510638	3.81403191489363
100 francs or napoléon III tête nue	2.0	14.5	12.5980138873392	2.01403899238363
1/10 oz krugerrand	3.0	12.9	12.966084626005	4.71340544871796
1/10 oz maple leaf	3.0	15.5	13.3649029492319	2.96617254273504
40 francs or napoléon empereur lauré	1.0	21.0	17.2714469877684	1.01863544605508
10 francs or cérès 1850-1851	5.0	25.0	19.8565988749459	4.71650885080078
10 francs or vreneli croix suisse	20.0	38.0	27.4068982718689	16.6249930339289
10 francs or coq marianne	7.0	30.0	30.6375898328164	15.8352219669118
"""


df = pd.read_csv(io.StringIO(data), sep='\t', header=None,
                 names=['Coin','Buy Prime (Seller)', 'Sell Prime (Seller)', 'Buy Prime (You)', 'Sell Prime (You)'])

# 1. Create DataFrames for seller and your data
seller_df = df[['Coin','Buy Prime (Seller)', 'Sell Prime (Seller)']].copy()
seller_df['Type'] = 'Seller'
your_df = df[['Coin','Buy Prime (You)', 'Sell Prime (You)']].copy()
your_df['Type'] = 'You'

# 2. Rename columns
seller_df = seller_df.rename(columns={'Buy Prime (Seller)': 'Buy Prime', 'Sell Prime (Seller)': 'Sell Prime'})
your_df = your_df.rename(columns={'Buy Prime (You)': 'Buy Prime', 'Sell Prime (You)': 'Sell Prime'})

# 3. Combine DataFrames
combined_df = pd.concat([seller_df, your_df])

# 4. Create the Altair Chart
chart = alt.Chart(combined_df).mark_circle(size=60).encode(
    x='Buy Prime:Q',
    y='Sell Prime:Q',
    color='Type:N',   # Use a nominal color scale for distinct categories
    tooltip=['Buy Prime:Q', 'Sell Prime:Q', 'Type:N','Coin:N']
).properties(
    title='Buy/Sell Premiums Comparison',
    width=1600,
    height=800,
).interactive()

# Combine the charts and display
chart.save('premium_comparison_scatter_plot_combined.html')
chart.save('premium_comparison_scatter_plot_combined.json')