# FindMeTunnel region data

The tunnels, bridges and metro lines that ship inside the iOS app [FindMeTunnel](https://apps.apple.com/app/id6817347414): 18,019 places in 126 regions of Europe, built from OpenStreetMap.

This database is derived from OpenStreetMap, so it is open under the same licence, the [Open Database License (ODbL) 1.0](LICENSE). Each release here matches one version of the app: the files are exactly the ones inside that build.

## Files

| File | What it is |
| --- | --- |
| `regions/<id>.json` | One region: a country, or a state/county of a larger one (`de-nw`, `it-25`, `no-46`) |
| `index.json` | List of regions with place counts by kind and data dates |
| `boundaries.json` | Simplified outline of each region, used by the app to suggest your home region |
| `tools/update.py` | Copies the files from an app checkout and rebuilds `index.json` |

## Region file

```json
{
  "version": 1,
  "id": "ad",
  "country": "AD",
  "name": { "en": "Andorra", "uk": "Андорра", "de": "Andorra" },
  "generated": "2026-11-04",
  "osm": "2026-11-02",
  "sources": "© OpenStreetMap contributors (ODbL); Copernicus DEM ...; Wikidata (CC0)",
  "bbox": [ ... ],
  "places": [ ... ]
}
```

`osm` is the date of the OpenStreetMap data the region was built from. Regions built in early October 2026 from the public Overpass API have no `osm` date; `generated` is the build date.

### Place

| Field | Meaning |
| --- | --- |
| `id` | `osm-<way id>`, or `osm-r<relation id>` for a metro line |
| `osm` | The OSM way (or relation) the place comes from |
| `kind` | `roadTunnel`, `railTunnel`, `bikeTunnel`, `carBridge`, `railBridge`, `footBridge`, `metroLine` |
| `length` | Metres along the line |
| `entry`, `exit` | `[lat, lon]` of the two ends (tunnel portals, bridge abutments, metro terminals) |
| `center` | `[lat, lon]` of the middle of the line |
| `name` | Own name of the structure (see below); absent when it has none |
| `latin` | Latin transliteration of a Cyrillic or Greek `name` |
| `ref` | Road number of the road on it |
| `year` | Opening year, from OSM or the structure's own Wikidata item |
| `wikidata` | Wikidata item of the structure itself, never of the road or line |
| `profile` | Terrain cross-section along the line (see below) |
| `articleSuppressed`, `articleReviewNote` | The Wikidata item is near but not this structure; the note says why |

Metro lines also have `stations`, `underground` (metres in tunnel), `terminals`, `network`, `city` (en/uk/de) and, where every station depth is known, `depth` (metres).

### Profile

Heights in metres above sea level, sampled evenly along `span` metres of terrain that includes the place and a bit around it.

| Field | Meaning |
| --- | --- |
| `kind` | `mountain` (tunnel under terrain), `bridge` (over a valley), `city` (metro) |
| `span` | Metres the profile covers |
| `ground` | Terrain heights along the span |
| `routeFrom`, `routeTo` | Where the place starts and ends, as a fraction of the span |
| `route` | Heights of the road or track between those two points |
| `marks` | Metro only: station positions, as fractions of the span |

Terrain heights come from the Copernicus DEM, not from OSM.

## What is included

- Tunnels: road from 150 m, rail from 200 m, cycle from 80 m.
- Footbridges from 100 m.
- Road and rail bridges from 300 m, and only with a name; from 100 m if the bridge has its own Wikidata item.
- Anything without its own name only from 500 m.
- Rail means `rail`, `subway`, `light_rail`, `narrow_gauge`, `tram`, `funicular`, `monorail`; platforms (`railway=platform`) are left out.
- Metro lines: `route_master=subway` whose tracks are mostly `railway=subway`, so Stadtbahn systems are left out.

Names come from `tunnel:name` or `bridge:name` first. A plain `name` is used only when it contains a word for tunnel or bridge in the region's languages, because on a rail tunnel it is often the name of the line, and on a bridge the name of the street. A big bridge often carries its name only on its `man_made=bridge` outline, so the road or track inside the outline takes that name. When OSM has no usable name, the label of the structure's own Wikidata item is used.
## Licence and attribution

- The database is licensed under the [ODbL 1.0](LICENSE), and its contents under the [Database Contents License 1.0](DBCL).
- Attribution: **© OpenStreetMap contributors**, plus the sources listed in each file's `sources` field:
  - Copernicus DEM © DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS by the European Union and ESA;
  - Wikidata (CC0);
  - metro station depths in `cz` and `ua` come from Wikipedia (CC BY-SA 4.0); those in `gb-eng`, from Transport for London (FOI-0493-2223).
- If you publish something built from this data, you have to keep it open under the ODbL too.

## Found a mistake?

Most mistakes here are mistakes in OpenStreetMap: a missing `tunnel:name`, a tunnel split into pieces, a wrong `wikidata` tag. Fixing them in OSM fixes them here with the next build. If the mistake is in how this data was built, open an issue with the place `id`.
