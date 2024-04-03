## Issues

| Issues | Details | Solutions |
| ----------- | ----------- | ----------- |
| Records too big | Got this error: `algoliasearch.exceptions.RequestException: Record at the position 32 objectID=51053ee5b8a30e406d2af85fe352981e is too big size=38069/10000 bytes.` Because there are size limits for records, some detailed activities exceed this limit. Please have a look at https://www.algolia.com/doc/guides/sending-and-managing-data/prepare-your-data/in-depth/index-and-records-size-and-usage-limitations/#record-size-limits | For now, use sys.getsizeof to filter our records over 10_000 bytes. Once we go premium, we can have records over 10kb, but need to average under 10kb for all records...**think about this**
| Unreachable host | While batch uploading the bw data, some batches would upload fine, some would fail with this error: `AlgoliaUnreachableHostException("Unreachable hosts")` | Fixed by adding a retry loop with a try/catch. If we hit this error, reset the connection (this is the fix), add a squick sleep to try and avoid any rate limiting, and try again. |

## Notes

We need to be able to search only certain fields to match existing functionality, we can do that with this:

```
results = index.search("someQuery", {'restrictSearchableAttributes': "name"})
```